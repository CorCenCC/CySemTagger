package uk.ac.lancs.ucrel.semtagger.welsh;

import java.io.Serializable;
import java.util.*;

/**
 * This is a semantic disambiguation context rule interface. The context rules
 * are to be provided from an external.
 *
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */
public class ContextRules implements Serializable {

    private Hashtable RULE_SET;
    private Vector sem_tag_vct;
    private Vector RULE_SET_VECTOR;
    private Vector TOK_KEYS = new Vector();
    private String[] TAG_KEYS;
    private int KEY_NUMBER;

    public ContextRules() {
        RULE_SET = new Hashtable();
        sem_tag_vct = new Vector();

        String engSemContextRulesPath = (String) UcrelCorcenccProperties.getInstance().getValue("eng.sem.context.rules");
        if (engSemContextRulesPath == null) {
            System.err.println("ERROR: Welsh semantic context rules file cannot be found.");
        }

        uploadContextRules(engSemContextRulesPath);
    }

    /**
     * If a word is passed, it checks if it is included in the key list. If the
     * input string is a key, it returns a boolean value.
     *
     * @param inkey A token or POS tag.
     * @return boolean value.
     */
    public boolean isKeyWord(String inkey) {
        if (Collections.binarySearch(TOK_KEYS, inkey) < 0) {
            return false;
        } else {
            RULE_SET_VECTOR = (Vector) RULE_SET.get(inkey);
            return true;
        }
    }

    /**
     * If a POS tag is passed, it checks if it is included in the key list.
     *
     * @param inkey A POS tag.
     * @return boolean value.
     */
    public boolean isKeyTag(String inkey) {

        for (int i = 0; i < TAG_KEYS.length; i++) {
            if (inkey.startsWith(TAG_KEYS[i])) {
                RULE_SET_VECTOR = (Vector) RULE_SET.get(TAG_KEYS[i]);
                return true;
            }
        }
        return false;
    }

    /**
     * For an input word_POS sequence, checks the matching context rules and
     * return them. This method can only be used when the isKey(.) method
     * returns "true" value.
     *
     * @param instr Word_POS sequence.
     * @return Matched context rules.
     */
    public Vector getSemTag(String instr) {
        for (int i = 0; i < RULE_SET_VECTOR.size(); i++) {
            String[] ss = (String[]) RULE_SET_VECTOR.get(i);
        }

        String[] rule_items;
        String rule, tag, udttok;
        for (int i = 0; i < RULE_SET_VECTOR.size(); i++) {
            rule_items = (String[]) RULE_SET_VECTOR.get(i);

            udttok = instr.replaceFirst(rule_items[0], " ");
            if (!udttok.equals(instr)) {

                Vector match_tag = new Vector();
                match_tag.addElement(rule_items[1]);
                return match_tag;
            }
        }
        return null;
    }

    /**
     * Loads the context rules from a file.
     */
    private void uploadContextRules(String ruleFilePath) {

        OpenSaveFile osf = new OpenSaveFile();

        List inrule = osf.getListOfLinesFromFile(ruleFilePath, "UTF8");
        if (inrule == null) {
            System.err.println("ERROR: Can not open the context rule file \"" + ruleFilePath + "\"");
        }

        String entry, key_token = "", key_tag = "";
        String[] items, key_toks;
        Vector tag_key_list = new Vector(), rule_entry;
        int indx;
        KEY_NUMBER = 0;
        for (int i = 0; i < inrule.size(); i++) {
            entry = (String) inrule.get(i);
            if (entry.startsWith("/*") || entry.trim().equals("")) {
                continue;
            }

            items = entry.split(" ");
            rule_entry = new Vector();
            for (int j = 0; j < items.length; j++) {
                if (items[j].endsWith("]")) {
                    indx = items[j].indexOf("[");
                    key_token = items[j].substring(0, indx).trim(); //Key Tokens

                    //System.out.print("keytok: " + key_token);
                    key_tag = items[j].substring(indx + 1, items[j].length() - 1);
                    //System.out.println("  keytok: " + key_tag);
                    rule_entry.addElement(convertToRegexp(key_token));
                } else {
                    rule_entry.addElement(convertToRegexp(items[j]));
                }
            }

            String[] passitems = key_token.split("[\\*\\_\\{\\}/]");
            String passkey;
            Vector rulevct;

            for (int j = 0; j < passitems.length; j++) {
                passkey = passitems[j].trim();
                if (passkey.equals("")) {
                    continue;
                }

                if (!TOK_KEYS.contains(passkey) && !tag_key_list.contains(passkey)) {
                    KEY_NUMBER++;
                    if (Character.isLowerCase(passkey.charAt(0))) {
                        TOK_KEYS.addElement(passkey);
                    } else {
                        tag_key_list.addElement(passkey);
                    }
                }

                rulevct = (Vector) RULE_SET.get(passkey);
                String[] map = {convertTemplate(rule_entry, 0).trim(), key_tag};
                //System.out.println("rule: " + map[0] + "; semtag: " + map[1]);
                if (rulevct == null) {
                    //System.out.println("key1: " + passkey + "; rule1: " + rule_entry.trim());
                    Vector pass_vct = new Vector();

                    pass_vct.addElement(map);
                    RULE_SET.put(passkey, pass_vct);
                } else {
                    //System.out.println("key2: " + passkey + "; rule2: " + rule_entry.trim());
                    rulevct.addElement(map);
                    RULE_SET.put(passkey, rulevct);
                }
            }

        }

        TOK_KEYS.trimToSize();
        Collections.sort(TOK_KEYS);
        //System.out.println(TOK_KEYS);
        TAG_KEYS = new String[tag_key_list.size()];
        for (int i = 0; i < tag_key_list.size(); i++) {
            TAG_KEYS[i] = (String) tag_key_list.get(i);
            //System.out.print(TAG_KEYS[i] + " ");
        }

    }

    /**
     * Convert each item into regular expression
     */
    private String convertToRegexp(String in_template) {

        if (in_template.startsWith("{")) {
            if (Character.isLowerCase(in_template.charAt(1))) { //Curly brackets contain word
                in_template = in_template.substring(1, in_template.length() - 1).replaceAll("[*]", "\\\\S*");
                return "((" + in_template + "_\\S+)\\s+)*?";
            }
            if (in_template.equals("{*}")) {
                return "((\\S+_\\S+)\\s+)*?";
            }
            in_template = in_template.toLowerCase();
            StringBuffer sb = new StringBuffer();
            sb.append("((");
            StringTokenizer splits = new StringTokenizer(in_template, "{/}");
            sb.append("(\\S*_" + splits.nextToken().replaceAll("[*]", "\\\\S*") + ")");
            while (splits.hasMoreTokens()) {
                sb.append("|(\\S*_" + splits.nextToken().replaceAll("[*]", "\\\\S*") + ")");
            }
            //Modified
            sb.append(")\\s+)*?");
            return sb.toString();
        } else if (in_template.startsWith("?")) { //For punctuation marks
            in_template = "\\".concat(in_template);
            return in_template.replaceAll("[*]", "\\\\S+");
        } else if (in_template.indexOf("*") >= 0) {
            return in_template.toLowerCase().replaceAll("[*]", "\\\\S*");
        } else {
            return in_template.toLowerCase();
        }
    }

    /**
     * Complete regular expression format
     */
    private String convertTemplate(Vector in_template, int flag) {
        StringBuffer sb = new StringBuffer();
        int loop = in_template.size();
        for (int i = 0; i < loop; i++) {
            String tktg = (String) in_template.get(i);
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

}
