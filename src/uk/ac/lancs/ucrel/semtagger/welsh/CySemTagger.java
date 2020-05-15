package uk.ac.lancs.ucrel.semtagger.welsh;

import java.io.File;
import java.util.StringTokenizer;
import java.util.List;
import java.util.ArrayList;

/**
 * Welsh semantic tagger based on Lancaster USAS. It uses CyTag for POS
 * annotation. It is developed for CorCenCC Project (http://www.corcencc.org/)
 *
 * For reference, please cite the paper below:
 *
 * Piao, Scott, Paul Rayson, Dawn Knight and Gareth Watkins (2018). Towards A
 * Welsh Semantic Annotation System. The 11th Edition of the Language Resources
 * and Evaluation Conference (LREC2018), Miyazaki, Japan.
 *
 * License: This is a free software. For the details of the license, see
 * LICENSE.txt file included in this package.
 *
 * @author Scott Piao (s.piao@lancaster.ac.uk).
 */
public class CySemTagger {

    private WelshPosMapCytag posMap;
    private List<String> N1_TAG;
    private List<String> N4_TAG;
    private List<String> vct;
    private WelshSemLexDict welshSemLex;
    private WelshMweDic welshMwes;
    private List<DataStructure> TAGGED_TEXT;
    private int MAX_MWE_LEN; //The maximum length of MWEs
    boolean IS_COMPOUND = false;
    private List<String> PUNCT_TAG;
    private CyTagWrapper welshPosTagger;

    /**
     * Constructor
     */
    public CySemTagger() {

        vct = new ArrayList<String>();
        MAX_MWE_LEN = 7; //Set the length of scanning window to 7 words by default.
        TAGGED_TEXT = new ArrayList<DataStructure>();
        //Semantic Puctuation tag
        PUNCT_TAG = new ArrayList<String>();
        PUNCT_TAG.add("PUNCT");
        N1_TAG = new ArrayList<String>();
        N1_TAG.add("N1");
        N4_TAG = new ArrayList<String>();
        N4_TAG.add("N4");

        //Initialise lexicon objects and POS tagger
        welshSemLex = new WelshSemLexDict();
        welshMwes = new WelshMweDic();
        posMap = new WelshPosMapCytag();
        welshPosTagger = new CyTagWrapper();

    }

    /**
     * Updated the maximum lengths of the multiword expressions to be
     * recognised.
     */
    public void setMaxMweLength(int mwe_len) {
        MAX_MWE_LEN = mwe_len;
    }

    /**
     * Returns semantically tagged text.
     *
     * @param fmtFlag Flag for format.
     * @param ins Input raw Welsh text.
     */
    public String annotateText(int fmtFlag, String inText) {

        List<String> txtList = welshPosTagger.posTagTextInList(inText);

        tagText(txtList);

        //Return the formated text.
        return formatText(fmtFlag, TAGGED_TEXT);

    }

    //Returns a division of a Vector.
    private List<DataStructure> getSubVector(List<DataStructure> inv, int from_indx, int to_indx) {
        List<DataStructure> v = new ArrayList<DataStructure>();
        for (int i = from_indx; i < to_indx; i++) {
            v.add((DataStructure) inv.get(i));
        }
        return v;
    }

    /**
     * Tags the input text and returns the tagged text.
     *
     * @param intxt Input text in vertical format.
     */
    private void tagText(String intxt) {

        TAGGED_TEXT.clear();

        StringTokenizer stk = new StringTokenizer(intxt, " \n");

        String[] toks = new String[stk.countTokens() + 1];
        String[] poses = new String[toks.length];
        String[] posesOrig = new String[toks.length];
        String[] lemmas = new String[toks.length];

        String line;
        String[] items;
        int loop = 0;
        while (stk.hasMoreTokens()) {
            line = stk.nextToken().trim();

            if (line.equals("")) {
                continue;
            }

            if (line.startsWith("<") || line.endsWith(">")) {
                toks[loop] = line;
                poses[loop] = "NULL";
                posesOrig[loop] = "NULL";
                lemmas[loop] = "NULL";
                //morphs[loop] = "NULL";
                continue;
            } else {

                items = line.split("\t");

                if (items.length != 3) {
                    continue;
                }

                toks[loop] = items[0];
                posesOrig[loop] = items[1];
                poses[loop] = posMap.mapPosFor(items[1]);
                //poses[loop] = items[1];

                //For test only
                //System.out.println(toks[loop] + " | " + posesOrig[loop] + " | " + poses[loop]);
                if (items[2].equals("<unknown>")) {
                    lemmas[loop] = items[0].toLowerCase();
                } else {
                    lemmas[loop] = items[2].toLowerCase();
                }

            }
            loop++;
        }

        int loop2, mwe_no = 0, jump, punc_indx;
        String[] mwe_candts = new String[MAX_MWE_LEN];
        String[] mwe_tok_candts = new String[MAX_MWE_LEN];
        String[] mwe_lem_candts = new String[MAX_MWE_LEN];
        String[] mwe_orig_pos_tags = new String[MAX_MWE_LEN];
        //String[] mwe_mphs = new String[MAX_MWE_LEN];
        String tag, mwe_str = "", mwe_tok_str = "", mwe_lem_str = "", mwe_morph_str = "", cntxt_rule_key, mwe_origtag_str = "";
        char letter;

        //System.out.println("loop = " + loop);
        List<String> semtag;
        //Keep tagged text in a vector.
        for (int i = 0; i < loop; i++) {

            //If the line is mark-up, keep it and continue.
            if (toks[i].startsWith("<")) {
                TAGGED_TEXT.add(new DataStructure(toks[i]));
                continue;
            }
            //If the token is punctuation mark, tag it and continue.
            if (poses[i].equals("punc")) {
                TAGGED_TEXT.add(new DataStructure(toks[i], lemmas[i], poses[i], posesOrig[i], PUNCT_TAG));
                continue;
            }

            if (poses.equals("num")) {
                TAGGED_TEXT.add(new DataStructure(toks[i], lemmas[i], poses[i], posesOrig[i], N1_TAG));
                continue;
            }

            jump = 0;

            /**
             * *****************************************************************
             * **No context rule for Welsh yet yet //Apply context rules if the
             * word/tag is in the context keylist. //Meanwhile it select the
             * sub-rule-set for the matched key.^^^
             * if(ctxt_rules.isKeyWord(toks[i].substring(0, k).toLowerCase()) ||
             * ctxt_rules.isKeyTag(toks[i].substring(k+1))) { String l_contxt =
             * "", r_contxt = "";
             *
             * String tk = toks[i].substring(0, k); String tg =
             * toks[i].substring(k+1);
             *
             * //Creating left context for(int j=1; j <=MAX_MWE_LEN; j++) {
             * if((i-j) < 0 || (i-j) <=CTXT_RULE_APP_INDX) break; l_contxt =
             * toks[i-j].concat(" " + l_contxt); } //Creating right context
             * for(int j=1; j <=MAX_MWE_LEN; j++) { if(i+j >= loop ||
             * toks[i+j].equals(toks[i])) break; r_contxt = r_contxt.concat(" "
             * + toks[i+j]); } CTXT_RULE_APP_INDX = i; //Record location of last
             * word considered.
             *
             * //If the context string matches anyone of the context rules, use
             * the tag, otherwise, go to next step. Vector stag =
             * ctxt_rules.getSemTag((l_contxt.trim() + " " + toks[i] + " " +
             * r_contxt.trim()).toLowerCase());
             * //System.out.println((l_contxt.trim() + " " + toks[i] + " " +
             * r_contxt.trim()).toLowerCase()); if(stag != null) { String
             * pass_lem = lemmatiser.getLemmaOf(tk, tg);
             * TAGGED_TEXT.addElement(new DataStructure2(tk, pass_lem, tg,
             * stag)); continue; } }
             * ****************************************************************
             */
            //determine maximum number of words to consider for MWE
            loop2 = i + MAX_MWE_LEN;
            if (loop2 >= loop) {
                loop2 = loop;
            }

            //System.out.println("loop2 = " + loop2);
            //Creating candidate MWEs
            int count = 0;

            //Use inflectional tokens to form MWE candidates
            //mwe_candts[0] = toks[i] + "_" + poses[i];
            //Use lemmas to form MWE candidates
            mwe_candts[0] = lemmas[i] + "_" + poses[i];
            mwe_tok_candts[0] = toks[i];
            mwe_lem_candts[0] = lemmas[i]; //This is just to keep lemma form of the tokens
            mwe_orig_pos_tags[0] = posesOrig[i];
            //mwe_mphs[0] = morphs[i]; //This is just to keep morphological features of Russian words

            for (int j = i + 1; j < loop2; j++) {
                //System.out.print(toks[j] + " ");
                if (poses[j].equals("punc")) {
                    break;
                }

                count++;

                //Use inflectional tokens to form MWE candidates
                // mwe_candts[count] = mwe_candts[count - 1].concat(" " + toks[j] + "_" + poses[j]);
                //Use lemmas to form MWE candidates
                mwe_candts[count] = mwe_candts[count - 1].concat(" " + lemmas[j] + "_" + poses[j]);
                mwe_orig_pos_tags[count] = mwe_orig_pos_tags[count - 1].concat(" " + posesOrig[j]);
                mwe_tok_candts[count] = mwe_tok_candts[count - 1].concat(" " + toks[j]);
                mwe_lem_candts[count] = mwe_lem_candts[count - 1].concat(" " + lemmas[j]);

                //Add original tags
                //mwe_mphs[count] = mwe_mphs[count - 1].concat(" " + morphs[j]);
            }

            //Search for MWE from the candidates
            tag = null;
            for (int j = count; j > 0; j--) {
                //System.out.println(mwe_candts[j].toLowerCase());
                tag = welshMwes.getTemplateSemTag(mwe_candts[j].toLowerCase());

                if (tag != null) {
                    mwe_str = mwe_candts[j];
                    mwe_tok_str = mwe_tok_candts[j];
                    mwe_lem_str = mwe_lem_candts[j];
                    mwe_origtag_str = mwe_orig_pos_tags[j];
                    //mwe_morph_str = mwe_mphs[j];
                    jump += j;
                    break;
                }
            }

            //If no MWE beginning from this token is found, tag it as single token.
            if (tag == null) {
                tagSingleToken(toks[i], lemmas[i], poses[i], posesOrig[i]);
            } //If MWE is found, let the pointer jump forward over MWE length
            else {
                //Print the MWE in proper format
                mwe_no++;
                printMwe(mwe_no, mwe_str, mwe_tok_str, mwe_lem_str, tag, mwe_origtag_str, welshMwes.getMatchedRule(), mwe_morph_str);
                i += jump;
            }

        }
    }

    /**
     * Tags the input text and returns the tagged text. The input text is the
     * output of Welsh POS tagger.
     *
     * @param inText Input text in a List.
     */
    private void tagText(List<String> inText) {

        TAGGED_TEXT.clear();

        String[] toks = new String[inText.size() + 1];
        String[] poses = new String[toks.length];
        String[] posesOrig = new String[toks.length];
        String[] lemmas = new String[toks.length];

        String[] items;
        int loop = 0;
        for (String line : inText) {

            if (line.equals("")) {
                continue;
            }

            if (line.startsWith("<") || line.endsWith(">")) {
                toks[loop] = line;
                poses[loop] = "NULL";
                posesOrig[loop] = "NULL";
                lemmas[loop] = "NULL";
                //morphs[loop] = "NULL";
                continue;
            } else {

                items = line.split("\t");

                if (items.length != 3) {
                    continue;
                }

                toks[loop] = items[0];
                posesOrig[loop] = items[1];
                poses[loop] = posMap.mapPosFor(items[1]);
                //poses[loop] = items[1];

                //For test only
                //System.out.println(toks[loop] + " | " + posesOrig[loop] + " | " + poses[loop]);
                if (items[2].equals("<unknown>")) {
                    lemmas[loop] = items[0].toLowerCase();
                } else {
                    lemmas[loop] = items[2].toLowerCase();
                }

            }
            loop++;
        }

        int loop2, mwe_no = 0, jump, punc_indx;
        String[] mwe_candts = new String[MAX_MWE_LEN];
        String[] mwe_tok_candts = new String[MAX_MWE_LEN];
        String[] mwe_lem_candts = new String[MAX_MWE_LEN];
        String[] mwe_orig_pos_tags = new String[MAX_MWE_LEN];
        //String[] mwe_mphs = new String[MAX_MWE_LEN];
        String tag, mwe_str = "", mwe_tok_str = "", mwe_lem_str = "", mwe_morph_str = "", cntxt_rule_key, mwe_origtag_str = "";
        char letter;

        //System.out.println("loop = " + loop);
        List<String> semtag;
        //Keep tagged text in a vector.
        for (int i = 0; i < loop; i++) {

            //If the line is mark-up, keep it and continue.
            if (toks[i].startsWith("<")) {
                TAGGED_TEXT.add(new DataStructure(toks[i]));
                continue;
            }
            //If the token is punctuation mark, tag it and continue.
            if (poses[i].equals("punc")) {
                TAGGED_TEXT.add(new DataStructure(toks[i], lemmas[i], poses[i], posesOrig[i], PUNCT_TAG));
                continue;
            }

            if (poses[i].equals("num")) {
                TAGGED_TEXT.add(new DataStructure(toks[i], lemmas[i], poses[i], posesOrig[i], N1_TAG));
                continue;
            }

            jump = 0;

            /**
             * *****************************************************************
             * **No context rule for Welsh yet yet //Apply context rules if the
             * word/tag is in the context keylist. //Meanwhile it select the
             * sub-rule-set for the matched key.^^^
             * if(ctxt_rules.isKeyWord(toks[i].substring(0, k).toLowerCase()) ||
             * ctxt_rules.isKeyTag(toks[i].substring(k+1))) { String l_contxt =
             * "", r_contxt = "";
             *
             * String tk = toks[i].substring(0, k); String tg =
             * toks[i].substring(k+1);
             *
             * //Creating left context for(int j=1; j <=MAX_MWE_LEN; j++) {
             * if((i-j) < 0 || (i-j) <=CTXT_RULE_APP_INDX) break; l_contxt =
             * toks[i-j].concat(" " + l_contxt); } //Creating right context
             * for(int j=1; j <=MAX_MWE_LEN; j++) { if(i+j >= loop ||
             * toks[i+j].equals(toks[i])) break; r_contxt = r_contxt.concat(" "
             * + toks[i+j]); } CTXT_RULE_APP_INDX = i; //Record location of last
             * word considered.
             *
             * //If the context string matches anyone of the context rules, use
             * the tag, otherwise, go to next step. Vector stag =
             * ctxt_rules.getSemTag((l_contxt.trim() + " " + toks[i] + " " +
             * r_contxt.trim()).toLowerCase());
             * //System.out.println((l_contxt.trim() + " " + toks[i] + " " +
             * r_contxt.trim()).toLowerCase()); if(stag != null) { String
             * pass_lem = lemmatiser.getLemmaOf(tk, tg);
             * TAGGED_TEXT.addElement(new DataStructure2(tk, pass_lem, tg,
             * stag)); continue; } }
             * ****************************************************************
             */
            //param = (String tok, String lem, String pos, Vector semcats)
            //determine maximum number of words to consider for MWE
            loop2 = i + MAX_MWE_LEN;
            if (loop2 >= loop) {
                loop2 = loop;
            }

            //Creating candidate MWEs
            int count = 0;

            //Use inflectional tokens to form MWE candidates
            //mwe_candts[0] = toks[i] + "_" + poses[i];
            //Use lemmas to form MWE candidates
            mwe_candts[0] = lemmas[i] + "_" + poses[i];

            mwe_tok_candts[0] = toks[i];
            mwe_lem_candts[0] = lemmas[i]; //This is just to keep lemma form of the tokens
            mwe_orig_pos_tags[0] = posesOrig[i];
            //mwe_mphs[0] = morphs[i]; //This is just to keep morphological features of Russian words

            for (int j = i + 1; j < loop2; j++) {
                //System.out.print(toks[j] + " ");
                if (poses[j].equals("punc")) {
                    break;
                }

                count++;

                //Use inflectional tokens to form MWE candidates
                // mwe_candts[count] = mwe_candts[count - 1].concat(" " + toks[j] + "_" + poses[j]);
                //Use lemmas to form MWE candidates
                mwe_candts[count] = mwe_candts[count - 1].concat(" " + lemmas[j] + "_" + poses[j]);

                //System.out.println(mwe_candts[count]);
                mwe_orig_pos_tags[count] = mwe_orig_pos_tags[count - 1].concat(" " + posesOrig[j]);
                mwe_tok_candts[count] = mwe_tok_candts[count - 1].concat(" " + toks[j]);
                mwe_lem_candts[count] = mwe_lem_candts[count - 1].concat(" " + lemmas[j]);

                //Add original tags
                //mwe_mphs[count] = mwe_mphs[count - 1].concat(" " + morphs[j]);
            }

            //Search for MWE from the candidates
            tag = null;
            for (int j = count; j > 0; j--) {
                if (mwe_candts[j].equals("pwyllgor_noun addysg_noun")) {
                    System.out.println(mwe_candts[j].toLowerCase());
                }
                tag = welshMwes.getTemplateSemTag(mwe_candts[j].toLowerCase());

                if (tag != null) {
                    mwe_str = mwe_candts[j];
                    mwe_tok_str = mwe_tok_candts[j];
                    mwe_lem_str = mwe_lem_candts[j];
                    mwe_origtag_str = mwe_orig_pos_tags[j];
                    //mwe_morph_str = mwe_mphs[j];
                    jump += j;
                    break;
                }
            }

            //If no MWE beginning from this token is found, tag it as single token.
            if (tag == null) {
                tagSingleToken(toks[i], lemmas[i], poses[i], posesOrig[i]);
            } //If MWE is found, let the pointer jump forward over MWE length
            else {
                //Print the MWE in proper format
                mwe_no++;
                printMwe(mwe_no, mwe_str, mwe_tok_str, mwe_lem_str, tag, mwe_origtag_str, welshMwes.getMatchedRule(), mwe_morph_str);
                i += jump;
            }

        }
    }

    private void printMwe(int index, String inmwe, String intok, String inlemmas, String intag, String inOrigTags, String tmrule, String morfFeatures) {

        String[] mwes = inmwe.split(" ");
        String[] tokens = intok.split(" ");
        String[] lems = inlemmas.split(" ");
        String[] origTagAry = inOrigTags.split(" ");
        //String[] mphs = morfFeatures.split(" ");
        String[] smtags = intag.split(" ");

        int mwe_len;

        //If no inserting tokens, assign every token with the intag.
        String token, postag, origPosTag;
        List<String> semTags;
        if (tmrule.indexOf("(") < 0) {
            //System.out.println("rule1: " + tmrule);

            mwe_len = mwes.length;
            for (int m = 0; m < mwes.length; m++) {
                int n = mwes[m].indexOf('_');

                postag = mwes[m].substring(n + 1);
                origPosTag = origTagAry[m];
                semTags = new ArrayList<String>(smtags.length);

                for (int k = 0; k < smtags.length; k++) {
                    semTags.add(smtags[k]);
                }

                TAGGED_TEXT.add(new DataStructure(tokens[m], lems[m], postag, origPosTag, semTags, index, mwe_len, m + 1));

            }
        } else { //If there is any embedded token(s), pick them out.
            //Split TM rule by space
            String[] tm = tmrule.split("(\\\\s\\+)|(\\*\\?)");

            //pick up literal rules - non-embedding tokens
            List<String> litrl_rules = new ArrayList<String>();
            for (int j = 0; j < tm.length; j++) {
                if (!tm[j].endsWith(")")) {
                    litrl_rules.add(tm[j]);
                }
            }
            //System.out.println("Literal Rules = " + litrl_rules + "\n");
            mwe_len = litrl_rules.size();
            int vct_sz = mwe_len, me_cnt = 0;
            boolean is_mwe;
            for (int m = 0; m < mwes.length; m++) {
                is_mwe = false;
                int n = mwes[m].indexOf('_');
                //token = mwes[m].substring(0, n);
                token = tokens[m];
                postag = mwes[m].substring(n + 1);
                origPosTag = origTagAry[m];
                //lemma = lemmatiser.getLemmaOf(token, postag);
                semTags = new ArrayList<String>(smtags.length);
                for (int k = 0; k < smtags.length; k++) {
                    semTags.add(smtags[k]);
                }

                //In case there are embedded words, check each token to determine if it is part of the MWE
                for (int j = 0; j < vct_sz; j++) {
                    //System.out.println(token + " <> " +
                    // (String)litrl_rules.get(j));
                    if ((mwes[m].toLowerCase()).matches((String) litrl_rules.get(j))) {
                        is_mwe = true;
                        me_cnt++;
                        litrl_rules.remove(j);
                        vct_sz--;
                        break;
                    }
                }

                if (is_mwe) {
                    TAGGED_TEXT.add(new DataStructure(token, lems[m], postag, origPosTag, semTags, index, mwe_len, me_cnt));
                } else {
                    TAGGED_TEXT.add(new DataStructure(token, lems[m], postag, origPosTag, welshSemLex.getSemanticTag(lems[m], postag)));
                }
            }
        }

    }

    private void tagSingleToken(String tok, String lem, String pos) {

        //System.out.println("item: " + tok + "_" + pos);
        List<String> semtag = welshSemLex.getSemanticTag(lem, pos);
        if (semtag.get(0).equals("Z99")) {
            semtag = welshSemLex.getSemanticTag(lem);
        }
        TAGGED_TEXT.add(new DataStructure(tok, lem, pos, semtag));
    }

    private void tagSingleToken(String tok, String lem, String pos, String origPos) {

        //System.out.println("item: " + tok + "_" + pos);
        List<String> semtag = welshSemLex.getSemanticTag(lem, pos);
        if (semtag.get(0).equals("Z99")) {
            semtag = welshSemLex.getSemanticTag(lem);
        }
        TAGGED_TEXT.add(new DataStructure(tok, lem, pos, origPos, semtag));
    }

    /**
     * Print semantic-tagged text in a specified format.
     *
     * @param flag Signifier for a format: 0 - xml format (single tag); 1 -
     * simplified TOKEN_TAG format; 2 - xml format with multiple tags). 3 - cwb
     * format
     * @return Formatted text.
     */
    private String formatText(int flag, List<DataStructure> text) {
        StringBuilder sb = new StringBuilder();
        if (flag == 0) { //XML format
            int size = text.size();
            for (int i = 0; i < size; i++) {
                DataStructure dts1 = text.get(i);
                String semtags = formatTags(dts1.SEMCATS);
                if (dts1.TOKEN.startsWith("<")) {
                    sb.append(dts1.TOKEN + "\n");
                } else if (!dts1.IS_MWE) {
                    sb.append("<w pos=\"" + dts1.POS + "\" mwe=\"0\" sem=\""
                            + semtags + "\" lem=\"" + dts1.LEMMA + "\">"
                            + dts1.TOKEN + "</w>\n");
                } else {
                    sb.append("<w pos=\"" + dts1.POS + "\" mwe=\""
                            + dts1.MWE_NO + ":" + dts1.MWE_INDEX[0] + ":"
                            + dts1.MWE_INDEX[1] + "\" sem=\"" + semtags
                            + "\" lem=\"" + dts1.LEMMA + "\">" + dts1.TOKEN
                            + "</w>\n");
                }
            }
        } else if (flag == 1) { //tok_tags format
            int size = text.size();
            for (int i = 0; i < size; i++) {
                DataStructure dts1 = (DataStructure) text.get(i);

                String semtags = formatTags(dts1.SEMCATS);

                if (dts1.TOKEN.equals("NULL")) {
                    sb.append("\n");
                    continue;
                } else if (dts1.TOKEN.startsWith("<")) {
                    sb.append("\n" + dts1.TOKEN + "\n");
                } else if (dts1.POS.startsWith("YS")
                        || dts1.POS.startsWith("YQ")
                        || dts1.POS.startsWith("YE")) {
                    sb.append(dts1.TOKEN + "_" + semtags + "\n");
                } else if (!dts1.IS_MWE) {
                    sb.append(dts1.TOKEN + "_" + semtags + " ");
                } else {
                    sb.append(dts1.TOKEN + "_[" + dts1.MWE_NO + ":"
                            //+ dts1.MWE_INDEX[0] + ":" + dts1.MWE_INDEX[1] + "]" +
                            // semtags.substring(0, semtags.indexOf(" ")) + " ");
                            + dts1.MWE_INDEX[0] + ":" + dts1.MWE_INDEX[1] + "]"
                            + semtags + " ");

                }
            }
        } else if (flag == 2) {
            int size = text.size();
            for (int i = 0; i < size; i++) {
                DataStructure dts1 = (DataStructure) text.get(i);

                String semtags = formatTags2(dts1.SEMCATS);

                if (dts1.TOKEN.startsWith("<")) {
                    sb.append(dts1.TOKEN + "\n");
                } else if (!dts1.IS_MWE) {
                    sb.append("<w pos=\"" + dts1.POS + "\" mwe=\"0\" sem=\""
                            + semtags + "\" lem=\"" + dts1.LEMMA + "\">"
                            + dts1.TOKEN + "</w>\n");
                } else {
                    sb.append("<w pos=\"" + dts1.POS + "\" mwe=\""
                            + dts1.MWE_NO + ":" + dts1.MWE_INDEX[0] + ":"
                            + dts1.MWE_INDEX[1] + "\" sem=\"" + semtags
                            + "\" lem=\"" + dts1.LEMMA + "\">" + dts1.TOKEN
                            + "</w>\n");
                }
            }
        } else { //CWB format
            int size = text.size();
            for (int i = 0; i < size; i++) {
                DataStructure dts1 = (DataStructure) text.get(i);

                //System.out.print(dts1.TOKEN + " ");
                String semtags = formatTags2(dts1.SEMCATS);

                if (dts1.TOKEN.startsWith("<")) {
                    sb.append(dts1.TOKEN + "\n");
                } else if (!dts1.IS_MWE) {
                    sb.append(dts1.TOKEN + "\t" + dts1.LEMMA + "\t" + dts1.POS
                            + "\t" + semtags + "\t"
                            + "0" + "\t" + dts1.POS_ORIG + "\n");
                } else {
                    sb.append(dts1.TOKEN + "\t" + dts1.LEMMA + "\t" + dts1.POS
                            + "\t" + semtags + "\t"
                            + dts1.MWE_NO + ":" + dts1.MWE_INDEX[0] + ":"
                            + dts1.MWE_INDEX[1] + "\t" + dts1.POS_ORIG + "\n");
                }

            }

        }

        return sb.toString();
    }

    /**
     * Print Semantic tags in a given specific format.
     *
     * @param v Vector containing possible semantic tags.
     * @return Semantic tags listed in the given specific format.
     */
    private String formatTags(List<String> v) {
        if (v == null) {
            return "Z99"; //Z99: unknown token
        } else {
            return (String) v.get(0);
        }
    }

    /**
     * Print all Semantic tags.
     *
     * @param v Vector containing possible semantic tags.
     * @return Semantic tags listed in the given specific format.
     */
    private String formatTags2(List<String> v) {
        if (v == null) {
            return "Z99"; //Z99: unknown token
        } else {
            int n = v.size();
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) {
                sb.append((String) v.get(i) + " ");
            }
            return sb.toString().trim();
        }
    }

    /**
     * For test only
     */
    public static void main(String[] args) {

        CySemTagger app = new CySemTagger();

        String text = "Yn enw'r \"Tad a'r Mab\" a'r Ysbryd Glân, Amen.";
        text = "Ystyrir yn gyffredinol mai ar gyfer pobl hŷn mae ein cynllun tocyn bws rhad ac am ddim, ond fe'i targedir hefyd at bobl ag anabledd.";
        String result = app.annotateText(3, text);
        System.out.println(result);

        /*
         OpenSaveFile osf = new OpenSaveFile();

         String dirPath = "/home/scott/Desktop/Programs/corcencc-test-space/cysemtagger-eval/evaluation-data/raw-gc-data-2/";
         File dir = new File(dirPath);
         File[] fs = dir.listFiles();

         for (File f : fs) {

         if (!f.getName().endsWith(".txt")) {
         continue;
         }

         String text = osf.getStringFromFile(f, "UTF8");
         text = app.annotateText(3, text);
            
         String outpath = f.getAbsolutePath().replace("raw-gc-data-2", "auto-tagged").replace(".txt", "-auto.csv");
            
         System.out.println(outpath);
            
         osf.saveTextToFile("TOTEN	LEM	POS-SIM	SEM	MWE	POS-FULL\n" + text + "\n", outpath, "UTF8");

         }
         */
    }

}
