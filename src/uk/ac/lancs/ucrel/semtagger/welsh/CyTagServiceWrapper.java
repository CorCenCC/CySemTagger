/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.lancs.ucrel.semtagger.welsh;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

/**
 * A client wrapper of CyTag Welsh POS tagger's web service developed in the CorCenCC Project [Add Cytag service URL].
 * 
 * It is developed for CorCenCC Project (http://www.corcencc.org/)
 * 
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */

public class CyTagServiceWrapper {
    
    private final String cyTagUrl = "http://cytag.corcencc.org/rest/pos/";
    
    public String welshTagger(String text) {
        try {
            String urlAndText = cyTagUrl + URLEncoder.encode(text, "UTF-8");
            
            URL url = new URL(urlAndText);
            HttpURLConnection uc = (HttpURLConnection) url.openConnection();
            InputStream content = uc.getInputStream();
            
            byte[] buf = new byte[1024];
            ByteArrayOutputStream sb = new ByteArrayOutputStream();
            int i = 0;
            while ((i = content.read(buf)) != -1) {
                sb.write(buf, 0, i);
            }

            content.close();
            return sb.toString();

        } catch (IOException ex) {
            return null;
        } 
    }
    
    //For test only.
    public static void main(String[] args) {
        
        String welshText = "Cymru am byth, dyma fy mrawd i +55.\n Cymru am byth, dyma fy mrawd i +55.";

        CyTagServiceWrapper app = new CyTagServiceWrapper();
        String output = app.welshTagger(welshText);
        
        System.out.println(output);
    }

}

