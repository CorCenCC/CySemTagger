/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.lancs.ucrel.semtagger.welsh;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

/**
 * This is Welsh semantic lexicon dictionary.
 *
 * It is developed for CorCenCC Project (http://www.corcencc.org/)
 * 
 * License: This is a free software. For the details of the license, see LICENSE.txt file included in this package.
 * 
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */
public class WelshSemLexDict {

    private Map<String, List> dictionary;
    private Map<String, List> dictionary2;
    private List<String> numTag;
    private List<String> z99Tag;
    //WelshPosMapLexTest lexPosMapTemp = new WelshPosMapLexTest();

    OpenSaveFile osf = new OpenSaveFile();

    public WelshSemLexDict() {

        String lexPath = (String) UcrelCorcenccProperties.getInstance().getValue("welsh.semlex.path");

        dictionary = new HashMap<String, List>();
        dictionary2 = new HashMap<String, List>();
        numTag = new ArrayList<String>();
        numTag.add("N1");
        z99Tag = new ArrayList<String>();
        z99Tag.add("Z99");

        //System.out.println(lexPath);
        loadSemanticLexicon(lexPath);
    }

    public List<String> getSemanticTag(String inTok, String inPos) {

        if (inPos.toLowerCase().equals("num")) {
            return numTag;
        }

        String key = inTok.toLowerCase() + "_" + inPos.toLowerCase();
        List<String> stags = dictionary.get(key);
        if (stags == null) {
            return z99Tag;
        } else {
            return stags;
        }
    }

    public List<String> getSemanticTag(String inTok) {
        List<String> stags = dictionary2.get(inTok);
        if (stags == null) {
            return z99Tag;
        } else {
            return stags;
        }
    }

    /**
     * Load Welsh semantic lexicon into dictionary; token (lemma later) and POS
     * tag provide the key.
     *
     * @param fpath File path to the Welsh semantic lexicon.
     */
    private void loadSemanticLexicon(String fpath) {

        //System.out.println(fpath);
        String itaLexicon = osf.getStringFromGzipFile(fpath, "UTF8");

        if (itaLexicon == null || itaLexicon.trim().equals("")) {
            System.err.println("ERROR: Cannot upload Welsh single-word Lexicon!");
            return;
        }

        //System.out.println(itaLexicon);
        StringTokenizer st = new StringTokenizer(itaLexicon, "\n");
        String line, key, semtags;
        List<String> semTagList;

        //StringBuilder sb = new StringBuilder();
        while (st.hasMoreTokens()) {
            line = st.nextToken().trim();

            if (line.startsWith("/*") || line.startsWith("//") || line.startsWith("#") || line.equals("")) {
                continue;
            }

            String[] items = line.split("\t");

            if (items.length != 3) {
                continue;
            }

            //String commonPosTag = lexPosMapTemp.mapPosFor(items[1]);
            key = items[0].toLowerCase() + "_" + items[1].toLowerCase();
            //key = items[0].toLowerCase() + "_" + commonPosTag.toLowerCase();

            semTagList = new ArrayList<String>();
            String[] stags = items[2].split(" ");
            for (int i = 0; i < stags.length; i++) {
                semTagList.add(stags[i]);
            }

            dictionary.put(key.toLowerCase(), semTagList);
            dictionary2.put(items[0].toLowerCase(), semTagList);

        }

    }

    public static void main(String[] args) {

        WelshSemLexDict app = new WelshSemLexDict();

        System.out.println(app.getSemanticTag("amdanaf", "prep"));

        System.out.println(app.getSemanticTag("amdanaf"));
    }

}
