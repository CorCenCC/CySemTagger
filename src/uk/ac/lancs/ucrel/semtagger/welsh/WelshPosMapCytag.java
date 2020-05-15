/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.lancs.ucrel.semtagger.welsh;

import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

/**
 * Class for mapping CyTag Welsh POS tags to the simpler common tags.
 *
 * It is developed for CorCenCC Project (http://www.corcencc.org/)
 * 
 * License: This is a free software. For the details of the license, see LICENSE.txt file included in this package.
 * 
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */
public class WelshPosMapCytag {

    private Map<String, String> welshTreeTaggerPosMap;

    public WelshPosMapCytag() {

        String posMapPath = (String) UcrelCorcenccProperties.getInstance().getValue("welsh.pos.tagmap.corcencc");
        if (posMapPath == null || posMapPath.trim().length() == 0) {
            System.err.println("Error: WNLT Welsh POS mapping file cannot be found.");
            return;
        }

        welshTreeTaggerPosMap = new HashMap<String, String>();

        boolean ok = loadPosTagMap(posMapPath);

        if (!ok) {
            System.err.println("Error: Welsh POS mapping file cannot be found.");
            return;
        }
    }

    public String mapPosFor(String inPos) {
        if (inPos.trim().length() == 0) {
            return null;
        }

        String newTag = welshTreeTaggerPosMap.get(inPos);
        if (newTag == null) { //If a tag is unknown, assume it is a foreign word.
            return "xx";
        } else {
            return newTag;
        }
    }

    private boolean loadPosTagMap(String fpath) {
        OpenSaveFile osf = new OpenSaveFile();
        String mapList = osf.getStringFromGzipFile(fpath, "UTF8");
        if (mapList == null || mapList.trim().equals("")) {
            return false;
        }

        StringTokenizer st = new StringTokenizer(mapList, "\n");
        String line;
        while (st.hasMoreTokens()) {
            line = st.nextToken().trim();

            if (line.startsWith("#") || line.equals("")) {
                continue;
            }

            String[] tagPair = line.split("\t");
            if (tagPair.length != 4) {
                continue;
            }

            welshTreeTaggerPosMap.put(tagPair[1], tagPair[0]);

        }
        return true;
    }

    public static void main(String[] args) {
        
        WelshPosMapCytag app = new WelshPosMapCytag();
        String tag = app.mapPosFor("Gwann");
        
        System.out.println(tag);
        
    }
    
    
}
