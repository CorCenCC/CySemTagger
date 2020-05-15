/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.lancs.ucrel.semtagger.welsh;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * This is Driver class of CySemTagger that receives input text from system
 * standard input.
 *
 * @author Scott Piao
 */
public class Drive {

    private CySemTagger tagger;

    public Drive() {
        tagger = new CySemTagger();
    }

    private boolean run() throws IOException {
        BufferedReader in = null;
        try {
            in = new BufferedReader(new InputStreamReader(System.in));

            if (!in.ready()) {
                System.err.println("Error: No input text. Pass Welsh text using pipeline.");
                return false;
            }

            String line;
            StringBuilder txt = new StringBuilder();
            while ((line = in.readLine()) != null) {
                txt.append(line + "\n");
            }

            String inText = txt.toString();
            String taggedText = "";
            if (inText.length() > 0) {
                taggedText = tagger.annotateText(3, inText);
            } else {
                System.err.println("Error: No input text.");
                return false;
            }

            in.close();
            System.out.println(taggedText);
            return true;

        } catch (IOException e) {
            System.err.println("IOException in reading input.");
            return false;

        }
    }

    public static void main(String[] args) {

        try {
            Drive driver = new Drive();

            boolean b = driver.run();
            if (b) {
                System.exit(0);
            } else {
                System.out.println("Error: CySemTagger experiences problem.");
                System.exit(1);
            }
        } catch (IOException ex) {
            Logger.getLogger(Drive.class.getName()).log(Level.SEVERE, null, ex);
        }

    }
}
