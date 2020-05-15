/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.lancs.ucrel.semtagger.welsh;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.StringTokenizer;
import java.util.Vector;

/**
 * This is Welsh Multiword Expressions (MWE) dictionary.
 *
 * It is developed for CorCenCC Project (http://www.corcencc.org/)
 *
 * License: This is a free software. For the details of the license, see
 * LICENSE.txt file included in this package.
 *
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */
public class WelshMweDic {

    private HashMap<String, String> literalMwes;
    private HashMap<Character, Vector<String>> alphTemplateMap;
    private static String MATCHED_TEMPLATE;
    private Vector<String[]> starDiv;
    private int alphabetSize;
    private List<Character> letters;
    private OpenSaveFile osf;

    /**
     * Constructor
     */
    public WelshMweDic() {

        MATCHED_TEMPLATE = null;
        literalMwes = new HashMap<>();
        starDiv = new Vector<>();
        alphTemplateMap = new HashMap();
        letters = new ArrayList<>();
        osf = new OpenSaveFile();
        alphabetSize = 0;

        String welshTemplatesPath = (String) UcrelCorcenccProperties.getInstance().getValue("welsh.mwe.lexicon.path");
        String welshAlphabetList = (String) UcrelCorcenccProperties.getInstance().getValue("welsh.alphabet.list.path");

        loadAlphabet(welshAlphabetList);
        loadMweLexicon(welshTemplatesPath);
    }

    /**
     * Returns a semantic tag for a given string. If no matched template found,
     * returns null.
     *
     * @param mwe Input string.
     * @return semantic tag/s.
     */
    public String getTemplateSemTag(String mwe) {

        return getSemCatFromTemplate(mwe);
    }

    /**
     * Returns the matched template rule.
     *
     * @return The matched template rule; if no rule is matched, returns null.
     */
    public String getMatchedRule() {
        return MATCHED_TEMPLATE;
    }

    /**
     * Load Welsh letters
     */
    private void loadAlphabet(String fPath) {

        List<String> alph = osf.getListOfLinesFromGzipFile(fPath, "UTF8");

        alphabetSize = alph.size();
        for (int j = 0; j < alphabetSize; j++) {
            Character let = new Character(((String) alph.get(j)).charAt(0));
            letters.add(let);
        }

    }

    /**
     * Load the MWE semantic lexicon.
     *
     * @param filePath File path to the MWE lexicon.
     */
    public void loadMweLexicon(String filePath) {

        StringBuilder sb = new StringBuilder();

        //To keep templates in divisions to speed up searching
        Vector[] templateDivs = new Vector[alphabetSize + 2];
        for (int i = 0; i < alphabetSize + 2; i++) {
            templateDivs[i] = new Vector();
        }

        List<String> templateEntries = osf.getListOfLinesFromGzipFile(filePath, "UTF8");

        String curLine, tempMap;
        int loop = templateEntries.size();
        for (int i = 0; i < loop; i++) {

            curLine = (templateEntries.get(i));

            if (curLine.startsWith("#") || curLine.startsWith("/*") || curLine.startsWith("//")) {
                continue;
            }

            Vector<String> template = new Vector<String>();
            Vector<String> semtags = new Vector<String>();
            String passSemtags = "";

            int templateLength = 0;

            StringTokenizer stk = new StringTokenizer(curLine, " \t\r");
            while (stk.hasMoreTokens()) {
                String item = stk.nextToken();

                if (item.indexOf("_") >= 0 || item.startsWith("{")) {
                    templateLength++;
                    item = convertToRegexp(item);

                    template.addElement(item);
                } else {
                    semtags.addElement(item);
                    passSemtags += " " + item;
                }

            }

            //If the template is literal token string without wildcards, put
            // them in separate HashMap.
            if (curLine.indexOf("*") < 0 && curLine.indexOf("{") < 0) {
                tempMap = convertTemplate(template, 1).trim();
                literalMwes.put(tempMap, passSemtags.trim().toUpperCase());

                sb.append("*****Template = " + tempMap + "\n");

                continue;
            }

            tempMap = convertTemplate(template, 0).trim();

            sb.append(tempMap + "\n");

            String[] templateMap = {tempMap, passSemtags.trim().toUpperCase()};

            int letIndx = alphabetIndex(Character.toLowerCase(curLine.charAt(0)));

            templateDivs[letIndx].addElement(templateMap);

        }

        starDiv = (Vector) templateDivs[0].clone();

        for (int i = 0; i <= alphabetSize; i++) {
            alphTemplateMap.put(new Character(alphabetForIndex(i)), templateDivs[i]);
        }
    }

    //get semantic tag from template for a given multi-word unit
    private String getSemCatFromTemplate(String inMwe) {
        if (inMwe.equals("")) {
            MATCHED_TEMPLATE = null;
            return null;
        }

        //1) First check in the literal MWE templates; it is HashMap, very fast.
        String stag = (String) literalMwes.get(inMwe);
        if (stag != null) {
            MATCHED_TEMPLATE = inMwe;
            return stag;
        }

        //2) If the previous search fails, search through templates starting
        // with asterinsk
        int loopSize = starDiv.size();
        for (int i = 0; i < loopSize; i++) {
            String[] map = (String[]) starDiv.get(i);
            String templRule = map[0];
            if (inMwe.matches(templRule)) {
                MATCHED_TEMPLATE = templRule;
                return map[1];
            }
        }

        //3) If the previous search fails, search through a division of
        // template rules;
        char chr = inMwe.charAt(0);
        Vector<String[]> curVct;

        //3.1) Check if the character is Welsh letter
        curVct = (Vector) alphTemplateMap.get(new Character(chr));

        //3.2) If it is not, go to the section containing all the remaining templates.
        if (curVct == null) {

            curVct = (Vector) alphTemplateMap.get(new Character('='));
        }

        //3.3) find the template in a specified division
        int loop = curVct.size();
        for (int i = 0; i < loop; i++) {
            String[] map = (String[]) curVct.get(i);
            String templRule = map[0];

            if (inMwe.matches(templRule)) {
                MATCHED_TEMPLATE = templRule;
                return map[1];
            }
        }

        //4) If no match found, return null.
        MATCHED_TEMPLATE = null;
        return null;
    }

    private String convertToRegexp(String inTemplate) {

        if (inTemplate.startsWith("{")) {

            if (inTemplate.equals("{*}")) {
                return "((\\S+_\\S+)\\s+)*?";
            }

            if (inTemplate.startsWith("{*_")) {

                return "(" + inTemplate.replaceAll("[{}]", "").toLowerCase().replaceAll("[*]", "\\\\S*") + ")*?";
            }

            boolean isWord = false;
            if (Character.isLowerCase(inTemplate.charAt(1))) {
                isWord = true;
            }

            inTemplate = inTemplate.toLowerCase();
            StringBuffer sb = new StringBuffer();
            sb.append("((");
            StringTokenizer splits = new StringTokenizer(inTemplate, "{/}");

            if (isWord) {
                sb.append("(" + splits.nextToken().replaceAll("[*]", "\\\\S*") + "_\\S*)");
            } else {
                sb.append("(\\S*_" + splits.nextToken().replaceAll("[*]", "\\\\S*") + ")");
            }

            while (splits.hasMoreTokens()) {
                //Test
                if (isWord) {
                    sb.append("|(" + splits.nextToken().replaceAll("[*]", "\\\\S*") + "_\\S*)");
                } else {
                    sb.append("|(\\S*_" + splits.nextToken().replaceAll("[*]", "\\\\S*") + ")");
                }
            }
            //Modified
            sb.append(")\\s+)*?");

            return sb.toString();
        } else if (inTemplate.indexOf("*") >= 0) {
            return inTemplate.toLowerCase().replaceAll("[*]", "\\\\S*");
        } else {
            return inTemplate.toLowerCase();
        }
    }

    /**
     * Complete regular expression format
     */
    private String convertTemplate(Vector inTemplate, int flag) {
        StringBuilder sb = new StringBuilder();
        int loop = inTemplate.size();
        for (int i = 0; i < loop; i++) {
            String tktg = (String) inTemplate.get(i);
            if (tktg.endsWith("*?")) {
                sb.append(tktg);
            } else {
                if (i < loop - 1) {
                    if (flag == 0) {
                        sb.append(tktg + "\\s+");
                    } else {
                        sb.append(tktg + " ");
                    }
                } else {
                    sb.append(tktg);
                }
            }
        }
        return sb.toString();
    }

    /**
     * Checks the letter, then returns the index of it in the letter Vector
     */
    private int alphabetIndex(char c) {
        Character chr = new Character(c);
        int indx = letters.indexOf(c);
        if (indx >= 0) {
            return indx;
        }
        return alphabetSize;
    }

    /**
     * get index for input letter
     */
    private Character alphabetForIndex(int id) {
        if (id < alphabetSize) {
            return (letters.get(id));
        } else {
            return '=';
        }
    }

    //For test only.
    public static void main(String args[]) {

        WelshMweDic app = new WelshMweDic();

        String tags = app.getTemplateSemTag("gofyn_verb cwestio_verb i_prep");

        System.out.println(tags);

    }

}
