package uk.ac.lancs.ucrel.semtagger.welsh;

import java.util.List;

/**This is a data structure for keeping part-of-speech and semantic information of each token.
 * 
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */

public class DataStructure {

    /**Constructor initialises variables.*/
    public DataStructure() {
        TOKEN = null;
        LEMMA = null;
        POS = null;
        SEMCATS = null;
        IS_MWE = false;
        //istagged = false;
    }

    public DataStructure(String tok) {
        TOKEN = tok;
        LEMMA = "";
        POS = "";
        SEMCATS = null;
        IS_MWE = false;
        //istagged = false;
    }

    /**Constructor initialises variables.
    @param tok Token.
    @param pos POS tag of token.
    @param semcats Possible semantic tags of the token in Vector.*/
    public DataStructure(String tok, String lem, String pos, List<String> semcats) {
        TOKEN = tok;
        LEMMA = lem;
        POS = pos;
        SEMCATS = semcats;
        IS_MWE = false;
    }

    /**Constructor initialises variables.
    @param tok Token.
    @param pos POS tag of token.
    @param semcats Possible semantic tags of the token in Vector.*/
    public DataStructure(String tok, String lem, String pos, String origPos, List<String> semcats) {
        TOKEN = tok;
        LEMMA = lem;
        POS = pos;
        POS_ORIG = origPos;
        SEMCATS = semcats;
        IS_MWE = false;
    }

    /**Constructor for Finnish compound.
    @param tok Token.
    @param pos POS tag of token.
    @param semcats Possible semantic tags of the token in Vector.
    @param compFlag Boolean flag for Finnish compound (this is always true).*/
    public DataStructure(String tok, String lem, String pos, List<String> semcats, boolean compFlag) {
        TOKEN = tok;
        LEMMA = lem;
        POS = pos;
        POS_ORIG = pos;
        SEMCATS = semcats;
        IS_MWE = false;
        IS_COMPOUND = compFlag;
    }

    /**Constructor initialises variables; to be used when record MWEs.
    @param tok Token.
    @param pos POS tag of token.
    @param semcats Possible semantic tags of the token in List.
    @param mwe_no Sequential number of MWE.
    @param mwe_len The length of MWE.
    @param mwe_indx Location of the token in the MWE.*/
    public DataStructure(String tok, String lem, String pos, List<String> semcats, int mwe_no, int mwe_len, int mwe_indx) {
        TOKEN = tok;
        LEMMA = lem;
        POS = pos;
        POS_ORIG = pos;
        SEMCATS = semcats;
        MWE_NO = mwe_no;
        MWE_INDEX[0] = mwe_len;
        MWE_INDEX[1] = mwe_indx;
        IS_MWE = true;
    }

    /**Constructor initialises variables; to be used when record MWEs.
    @param tok Token.
    @param pos POS tag of token.
    @param semcats Possible semantic tags of the token in List.
    @param mwe_no Sequential number of MWE.
    @param mwe_len The length of MWE.
    @param mwe_indx Location of the token in the MWE.*/
    public DataStructure(String tok, String lem, String pos, String origPos, List<String> semcats, int mwe_no, int mwe_len, int mwe_indx) {
        TOKEN = tok;
        LEMMA = lem;
        POS = pos;
        POS_ORIG = origPos;
        SEMCATS = semcats;
        MWE_NO = mwe_no;
        MWE_INDEX[0] = mwe_len;
        MWE_INDEX[1] = mwe_indx;
        IS_MWE = true;
    }


    /**Updates token.
    @param token Input token.*/
    public void setToken(String token) {
        TOKEN = token;
    }

    /**Updates semantic tag.
    @param semtags Semantic from lexicon*/
    public void setSemTag(List<String> semtags) {
        SEMCATS = semtags;
    }

    /**Updates lemma of the token*/
    public void setLemma(String in_lem) {
        LEMMA = in_lem;
    }

    /**Updates base POS tag*//*
    public void setBasePos(String in_basepos) {
    BASE_POS = in_basepos;
    }*/

    /**Indicated is the token is tagged or not.
    @param state State of the token being tagged.
    public void tagged(boolean state) {
    istagged = state;
    }*/
    /**Record location index of this tok in MWE.
    @length Length of template.
    @locat location of a given item in the template.*/
    public void putMweIndex(int length, int locat) {
        MWE_INDEX[0] = length;
        MWE_INDEX[1] = locat;
    }
    /**Token.*/
    public String TOKEN;
    /**Basic form, lemma, of the input token*/
    public String LEMMA;
    /**Working POS tag */
    public String POS;
    /**Original POS tag */
    public String POS_ORIG;
    /**List of Possible semantic tags.*/
    public List SEMCATS;
    /**List of Possible semantic tags.*/
    public boolean IS_MWE; //default value: null
    /**List of Possible semantic tags.*/
    public boolean IS_COMPOUND = false; //default value: FALSE
    /**Record the index of an item within a MWE in a two element array: 1st = length of the MWE;
    2nd = location of the item in the MWE.*/
    public int[] MWE_INDEX = new int[2];
    /**Number of MWE.*/
    public int MWE_NO = 0;
}
