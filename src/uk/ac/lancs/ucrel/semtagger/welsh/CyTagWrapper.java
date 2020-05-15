/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.lancs.ucrel.semtagger.welsh;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

/**
 * This is a wrapper of the CyTag Welsh POS tagger (CyTag URL here).
 *
 * It is developed for CorCenCC Project (http://www.corcencc.org/)
 * 
 * License: This is a free software. For the details of the license, see LICENSE.txt file included in this package.
 * 
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */
public class CyTagWrapper {

    private String posTagger;
    private final String cyTagPath;
    private OpenSaveFile osf;
    private String encodeName;

    public CyTagWrapper() {
        cyTagPath = (String) UcrelCorcenccProperties.getInstance().getValue("welsh.cytag.path");

        if (cyTagPath == null) {
            System.err.println("CyTag path cannot be found: " + cyTagPath);
            System.exit(1);
        }

        posTagger = "CyTag.py";
        encodeName = "UTF8";
        osf = new OpenSaveFile();

        //System.out.println(cyTagPath);
    }

    /**
     * POS-tag the input Welsh text and return the result as a String.
     *
     * @param text Input Welsh raw text.
     * @return POS-tagged text.
     */
    public String posTagText(String text) {

        String inFilePath = cyTagPath + "cytag_input.temp";

        File inFile = new File(inFilePath);
        
        osf.saveTextToFile(text, inFilePath, encodeName);
        String tokedText = posTagFile(inFilePath);

        inFile.delete();

        return tokedText;
    }

    /**
     * POS-tag the input Welsh text and return the result as a String List.
     *
     * @param text Input Welsh raw text.
     * @return POS-tagged text.
     */
    public List<String> posTagTextInList(String text) {

        String taggedText = posTagText(text);

        if(taggedText == null) {
            return null;
        }
        
        List<String> posTaggedWordList = new ArrayList<>();

        StringTokenizer posTokenList = new StringTokenizer(taggedText, "\n");
        while(posTokenList.hasMoreTokens()) {
            
            String line = posTokenList.nextToken().trim();
            if(line.length()==0) {
                continue;
            }
            
            String[] columns = line.split("\t");
            
            //Pick up token, POS-tag and lemma.
            posTaggedWordList.add(columns[1] + "\t" + columns[5] + "\t" + columns[3]);
        }
        
        return posTaggedWordList;
    }
    
    
    
    /**
     * POS-tag the input text from the input file and return the result as a String.
     * 
     * @param filePath Absolute path to the input file.
     * @return POS-Tagged text.
     */
    public String posTagFile(String filePath) {
        
        File file = new File(filePath);
        if (!file.exists()) {
            System.err.println("Cannot open file: " + filePath);
            return null;
        }

        try {
            List<String> command = new ArrayList<>();
            command.add("bash");
            command.add("-c");
            command.add("cat " + filePath + " | " + "python3 " + cyTagPath + posTagger);

            ProcessBuilder builder = new ProcessBuilder(command);
            Process proc1 = builder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(proc1.getInputStream(), this.encodeName));

            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line.trim() + "\n");
            }

            proc1.waitFor();
            proc1.destroy();

            String taggedText = sb.toString();

            return taggedText;

        } catch (InterruptedException | IOException ex) {
            return null;
        }

    }
    
  

    /**
     * POS-tag the input text and return the result as a String.
     *
     * @param text Input Welsh text.
     * @return POS-Tagged text.
     */
    public String tagText(String text) {

        try {
            List<String> command = new ArrayList<>();
            command.add("bash");
            command.add("-c");
            command.add("python3 " + cyTagPath + posTagger + " < '" + text + "'");

            ProcessBuilder builder = new ProcessBuilder(command);
            
            Process proc1 = builder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(proc1.getInputStream(), this.encodeName));

            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line.trim() + "\n");
            }

            proc1.waitFor();
            proc1.destroy();

            String taggedText = sb.toString();

            return taggedText;

        } catch (InterruptedException | IOException ex) {
            return null;
        }
    }

    public static void main(String[] args) {

        CyTagWrapper app = new CyTagWrapper();

        String input = "Yn enw'r \"Tad a'r Mab\" a'r Ysbryd Glân, Amen.";
        String output = app.posTagText(input);

        System.out.println(output);

    }

}
