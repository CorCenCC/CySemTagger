/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.lancs.ucrel.semtagger.welsh;

import java.io.*;
import java.util.List;
import java.util.ArrayList;
import java.util.StringTokenizer;
import java.util.Arrays;
import java.util.zip.GZIPInputStream;

/**
 * This is an auxiliary class for opening files and saving texts into files.
 *
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */
public class OpenSaveFile {

    /**
     * Saves an input text into a specified file.
     *
     * @param txstr an String to be saved.
     * @param f a file path to save the input String.
     */
    public void saveTextToFile(String txstr, File f) {
        try {
            Writer outf;
            outf = new OutputStreamWriter(new FileOutputStream(f));
            outf.write(txstr);
            outf.close();
        } catch (IOException e) {
            System.err.println("Error: Cannot save input text into file: " + f.getAbsolutePath());
        }
    }

    /**
     * Saves an input text into a specified file.
     *
     * @param text an String to be saved.
     * @param fname a file name in String including path.
     */
    public void saveTextToFile(String text, String fname) {
        File file = new File(fname);
        if (file.getName().equals("")) {
        } else {
            try {
                Writer outf;
                outf = new OutputStreamWriter(new FileOutputStream(file));

                outf.write(text);
                outf.close();
            } catch (IOException e) {
                System.err.println("Error: Cannot save input text into file: " + fname);
            }
        }
    }

    /**
     * Saves an input text into a specified file with specified encoding.
     *
     * @param text A String to be saved.
     * @param fname A file name in String including path.
     * @param encode An encoding name.
     */
    public void saveTextToFile(String text, String fname, String encode) {
        File file = new File(fname);
        if (file.getName().equals("")) {
            System.err.println("Error: Cannot save input text into file: " + fname);
        } else {
            try {
                Writer outf;
                outf = new OutputStreamWriter(new FileOutputStream(file), encode);

                outf.write(text);
                outf.close();
            } catch (IOException e) {
                System.err.println("Error: Cannot save input text into file: " + fname);
            }
        }
    }

    /**
     * Saves an input text into a specified file.
     *
     * @param text an String to be saved.
     * @param f a File to save the input String.
     * @param encode a encoding name suppoted by Java from version 1.3.
     */
    public void saveTextToFile(String text, File f, String encode) {

        try {
            Writer outf;
            outf = new OutputStreamWriter(new FileOutputStream(f), encode);
            outf.write(text);
            outf.close();
        } catch (IOException e) {
            System.err.println("Error: Cannot save input text into file: " + f.getAbsolutePath());
        }
    }

    /**
     * Saves an object into a file.
     *
     * @param object An Java Bbject to be saved.
     * @param f File to which the input object is saved.
     */
    public void saveObjectToFile(Object object, File f) {

        try {
            ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(f));
            out.writeObject(object);
            out.close();
        } catch (Exception e) {
            System.err.println("Error: Cannot save input object into file: " + f.getAbsolutePath());
        }
    }

    /**
     * Saves an object into a file.
     *
     * @param object An Java Bbject to be saved.
     * @param fPath String file path to which the input object is saved.
     */
    public void saveObjectToFile(Object object, String fPath) {

        try {
            ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(fPath));
            out.writeObject(object);
            out.close();
        } catch (Exception e) {
            return;
        }
    }

    /**
     * Returns the contents of an output file in String.
     *
     * @param f an output File.
     * @return a String containing the contents of the input file.
     */
    public String getStringFromFile(File f) {
        StringBuilder str = new StringBuilder();
        try {
            InputStreamReader is = new InputStreamReader(new FileInputStream(f));
            Reader ins = new BufferedReader(is);
            int ch;
            while ((ch = ins.read()) > -1) {
                str.append((char) ch);
            }
            ins.close();
        } catch (IOException e) {
            return null;
        }
        return str.toString();
    }

    /**
     * Returns the contents of an output file in String.
     *
     * @param fname an output file name in String.
     * @return a String containing the contents of the input file.
     */
    public String getStringFromFile(String fname) {

        StringBuilder str = new StringBuilder();
        try {
            File f = new File(fname);
            InputStreamReader is = new InputStreamReader(new FileInputStream(f));
            try (Reader ins = new BufferedReader(is)) {
                int ch;
                while ((ch = ins.read()) > -1) {
                    str.append((char) ch);
                }
            }
        } catch (IOException e) {

            return null;
        }
        return str.toString();
    }

    /**
     * Reads the specified encoding and returns the contents of an output file
     * in String .
     *
     * @param f an output File.
     * @param Encode name of the encoding in which the output file is written.
     * @return a String containing the contents of the input file.
     */
    public String getStringFromFile(File f, String Encode) {

        StringBuilder str = new StringBuilder();
        try {
            InputStreamReader is = new InputStreamReader(new FileInputStream(f), Encode);
            Reader ins = new BufferedReader(is);
            int ch;
            while ((ch = ins.read()) > -1) {
                str.append((char) ch);
            }
            ins.close();
        } catch (IOException e) {
            return null;
        }
        return str.toString();
    }

    
    /**
     * Read Gun-zipped file.
     * 
     * @param f File object.
     * @param Emcode Encoding name, e.g. "UTF8".
     * @return Opened file as String. 
     */
     public String getStringFromGzipFile(File f, String Encode) {

        StringBuilder str = new StringBuilder();
        try {
            InputStreamReader is = new InputStreamReader(new GZIPInputStream(new FileInputStream(f)), Encode);
            Reader ins = new BufferedReader(is);
            int ch;
            while ((ch = ins.read()) > -1) {
                str.append((char) ch);
            }
            ins.close();
        } catch (IOException e) {
            return null;
        }
        return str.toString();
    }
    
    
    /**
     * Reads the specified encoding and returns the contents of an output file
     * in String .
     *
     * @param f an output File.
     * @param Encode name of the encoding in which the output file is written.
     * @return a String containing the contents of the input file.
     */
    public String getStringFromFile(String f, String Encode) {

        StringBuilder str = new StringBuilder();
        try {
            InputStreamReader is = new InputStreamReader(new FileInputStream(f), Encode);
            Reader ins = new BufferedReader(is);
            int ch;
            while ((ch = ins.read()) > -1) {
                str.append((char) ch);
            }
            ins.close();
        } catch (IOException e) {
            return null;
        }
        return str.toString();
    }

    /**
     * Read Gun-zipped file.
     * 
     * @param f Full file path.
     * @param Emcode Encoding name, e.g. "UTF8".
     * @return Opened file as String. 
     */
     public String getStringFromGzipFile(String f, String Encode) {

        StringBuilder str = new StringBuilder();
        try {
            InputStreamReader is = new InputStreamReader(new GZIPInputStream(new FileInputStream(f)), Encode);
            Reader ins = new BufferedReader(is);
            int ch;
            while ((ch = ins.read()) > -1) {
                str.append((char) ch);
            }
            ins.close();
        } catch (IOException e) {
            return null;
        }
        return str.toString();
    }
    
    
    /**
     * Reads an array of output files and returns the contents in String in
     * extended ASCII.
     *
     * @param f an File array to be read.
     * @return a String containing the contents of the input file.
     */
    public String getStringFromFiles(File[] f) {
        StringBuilder str = new StringBuilder();
        for (int i = 0; i < f.length; i++) {
            str.append(getStringFromFile(f[i]) + "\n\n");
        }
        return str.toString();
    }

    
    
    
    
    
    
    /**
     * Reads the specified encoding and returns the contents of an array of
     * output files in String .
     *
     * @param f an File array to be read.
     * @param encode name of the encoding in which the output file is written.
     * @return a String containing the contents of the input file.
     */
    public String getStringFromFiles(File[] f, String encode) {

        StringBuilder str = new StringBuilder();
        for (int i = 0; i < f.length; i++) {
            str.append(getStringFromFile(f[i], encode) + "\n\n");
        }
        return str.toString();
    }

    /**
     * Merges and returns the contents of the files under the directory
     * specified by the passing File.
     *
     * @param dr a File specifying a directory.
     * @return a String containing merged contents of all the files under the
     * specified directory.
     */
    public String getStringOfFilesInDirectory(File dr) {

        String f_list[] = dr.list();
        if (f_list.length == 0) {
            System.out.println("No Directory or File Is Chosen!\n");
            return null;
        }
        Arrays.sort(f_list);
        StringBuilder txts = new StringBuilder();
        int file_number = 0;
        for (String f_list1 : f_list) {
            File file = new File(dr, f_list1);
            if (file.isFile()) {
                file_number++;
                txts.append(getStringFromFile(file) + "\n");
            }
        }

        if (file_number > 0) {
            return txts.toString();
        } else {
            return null;
        }
    }

    /**
     * Reads text file included in a Jar file.
     *
     * @param filePath Directory path of a file.
     * @param encode An encoding name.
     * @return Content of the file in String.
     */
    public String getTextFromJar(String filePath, String encode) {
        String line;
        try {
            InputStream is = getClass().getResourceAsStream(filePath);
            BufferedReader br = new BufferedReader(new InputStreamReader(is, encode));

            StringBuilder sb = new StringBuilder();
            while ((line = br.readLine()) != null) {
                sb.append(line + "\n");
            }
            return sb.toString();
        } catch (Exception e) {
            return null;
        }
    }

    /**
     * Extracts an object from the given file.
     *
     * @param f an File array to be read.
     * @return An Obejct extracted from the file.
     */
    public Object getObjectFromFile(File f) {

        try {
            ObjectInputStream in = new ObjectInputStream(new FileInputStream(f));
            Object ojt = (Object) in.readObject();
            in.close();
            return ojt;
        } catch (ClassNotFoundException | IOException e) {
            return null;
        }
    }

    /**
     * Extracts an object from the given file.
     *
     * @param fPath String file path.
     * @return an Obejct extracted from the file.
     */
    public Object getObjectFromFile(String fPath) {

        try {
            ObjectInputStream in = new ObjectInputStream(new FileInputStream(fPath));
            Object ojt = (Object) in.readObject();
            in.close();
            return ojt;
        } catch (ClassNotFoundException | IOException e) {
            return null;
        }
    }

    /**
     * Opens the input file and put lines into a Vector and return the Vector.
     *
     * @param f a initialised File
     * @return a List containing the lines of the input file.
     */
    public List<String> getListOfLinesFromFile(File f) {

        String str = getStringFromFile(f);

        if (str == null) {
            return null;
        }

        StringTokenizer st = new StringTokenizer(str, "\n\r");
        List<String> v = new ArrayList<>();
        while (st.hasMoreTokens()) {
            String next_tok = st.nextToken();
            if (next_tok.trim().equals("")) {
                continue;
            }
            v.add(next_tok);
        }
        return v;
    }

    /**
     * Opens the input file and put lines into a Vector and return the Vector.
     *
     * @param fname a file name in String including path
     * @return a List containing the lines of the input file.
     */
    public List<String> getListOfLinesFromFile(String fname) {

        String str = getStringFromFile(fname);

        if (str == null) {
            return null;
        }

        StringTokenizer st = new StringTokenizer(str, "\n\r");
        List<String> v = new ArrayList<>();
        while (st.hasMoreTokens()) {
            String next_tok = st.nextToken().trim();
            if (next_tok.equals("")) {
                continue;
            }
            v.add(next_tok);
        }
        return v;
    }

    /**
     * Opens the input file and put lines into a Vector and return the Vector.
     *
     * @param fname a file name in String including path
     * @param encode Encoding used
     * @return a List containing the lines of the input file.
     */
    public List<String> getListOfLinesFromFile(String fname, String encode) {

        String str = getStringFromFile(fname, encode);
        if (str == null) {
            return null;
        }

        StringTokenizer st = new StringTokenizer(str, "\n\r");
        List<String> v = new ArrayList<>();
        while (st.hasMoreTokens()) {
            String next_tok = st.nextToken().trim();
            if (next_tok.equals("")) {
                continue;
            }
            v.add(next_tok);
        }
        return v;
    }
    
    public List<String> getListOfLinesFromGzipFile(String fname, String encode) {

        String str = getStringFromGzipFile(fname, encode);
        if (str == null) {
            return null;
        }

        StringTokenizer st = new StringTokenizer(str, "\n\r");
        List<String> v = new ArrayList<>();
        while (st.hasMoreTokens()) {
            String next_tok = st.nextToken().trim();
            if (next_tok.equals("")) {
                continue;
            }
            v.add(next_tok);
        }
        return v;
    }
    

    /**
     * Opens the input file and put lines into a Vector and return the Vector.
     *
     * @param f a file name in String including path
     * @param encode Encoding used
     * @return a List containing the lines of the input file.
     */
    public List<String> getListOfLinesFromFile(File f, String encode) {

        String str = getStringFromFile(f, encode);
        if (str == null) {
            return null;
        }

        StringTokenizer st = new StringTokenizer(str, "\n\r");
        List<String> v = new ArrayList<>();
        while (st.hasMoreTokens()) {
            String next_tok = st.nextToken().trim();
            if (next_tok.equals("")) {
                continue;
            }
            v.add(next_tok);
        }
        return v;
    }
    
    
    public List<String> getListOfLinesFromGzipFile(File f, String encode) {

        String str = getStringFromGzipFile(f, encode);
        if (str == null) {
            return null;
        }

        StringTokenizer st = new StringTokenizer(str, "\n\r");
        List<String> v = new ArrayList<>();
        while (st.hasMoreTokens()) {
            String next_tok = st.nextToken().trim();
            if (next_tok.equals("")) {
                continue;
            }
            v.add(next_tok);
        }
        return v;
    }
    
    
    

    /**
     * Opens the a file from JAR and put lines into a Vector and return the
     * Vector.
     *
     * @param fname a file name in String including path
     * @param encode Encoding used
     * @return a List containing the lines of the input file.
     */
    public List<String> getListOfLinesFromJar(String fname, String encode) {

        String str = getTextFromJar(fname, encode);

        if (str == null) {
            return null;
        }

        StringTokenizer st = new StringTokenizer(str, "\n\r");
        List<String> v = new ArrayList<>();
        while (st.hasMoreTokens()) {
            String next_tok = st.nextToken();
            if (next_tok.trim().equals("")) {
                continue;
            }
            v.add(next_tok);
        }
        return v;
    }
}
