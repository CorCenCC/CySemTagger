package uk.ac.lancs.ucrel.semtagger.welsh;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * This is aresource manager that controls resource paths. By editing the file "ucrelcorcencc.properties" included in the package, 
 * users can reset the resource paths.
 * 
 * It is developed for CorCenCC Project (http://www.corcencc.org/)
 *
 * License: This is a free software. For the details of the license, see
 * LICENSE.txt file included in this package.
 *
 * @author Scott Piao (s.piao@lancaster.ac.uk, scottpiao3@gmail.com).
 */
public class UcrelCorcenccProperties {

    private Properties properties;
    private final String PROPERTIES_FILE = "ucrelcorcencc.properties";
    private static UcrelCorcenccProperties _ref = null;

    public UcrelCorcenccProperties() {
        this.properties = new Properties();
        this.loadProperties();
    }

    private void loadProperties() {
        try {
            InputStream is = this.getClass().getClassLoader().getResourceAsStream(this.PROPERTIES_FILE);
            this.properties.load(is);
            is.close();
        } catch (IOException e) {
            return;
        }
    }

    public Object getValue(String property) {
        if (this.properties.containsKey(property)) {
            return this.properties.getProperty(property);
        } else {
            return null;
        }
    }

    public static UcrelCorcenccProperties getInstance() {
        if (_ref == null) {
            _ref = new UcrelCorcenccProperties();
        }
        return _ref;
    }

}
