# CySemTagger
This repo holds the rule based semantic tagger by Scott Piao as part of the CorCenCC project.

# Software Description

[Last updated: 21 March 2018]

This Welsh Semantic Tagger, named CySemTagger, is developed in Lancaster University, UK for the CorCenCC Project (http://www.corcencc.org/) based on Lancaster USAS framework (http://ucrel.lancs.ac.uk/usas/).

This version of software is dependent on Welsh POS tagger, CyTag (URL to CyTag). Therefore, users need to pre-install CyTag (including all dependencies), following one of the options below:
1) Download and install CyTag in the provided folder "ext-tools/CyTag-work-version/". Then the tool can automatically link to CyTag.
2) Download and install CyTag in any directory in your machine. Then adjust the property parameter "welsh.cytag.path" in the file "src/ucrelcorcencc.properties" to point to the CyTag's installation folder, then re-compile the package. If you adjust the parameter within the Jar file using an archive manager, no need to re-compile the package.

This tool receives input text using pipeline. For example, if your input text is in file "sample-text.txt", use one of the following commands:
1) >cat sample-text.txt | java -jar CySemTagger.jar, OR
2) >java -jar CySemTagger.jar < sample-text.txt

This version is licensed under GPLv3. For the corpyright statement, see file LICENSE.txt

For reference to this tool, please cite the following papers:
1) Piao, Scott, Paul Rayson, Dawn Knight and Gareth Watkins (2018). Towards A Welsh Semantic Annotation System. The 11th Edition of the Language Resources and Evaluation Conference (LREC2018), Miyazaki, Japan. 
2) Piao, Scott, Paul Rayson, Dawn Knight, Gareth Watkins and Kevin Donnelly (2017). Towards a Welsh Semantic Tagger: Creating Lexicons for A Resource Poor Language. In Proceedings of The Corpus Linguistics 2017 Conference, held from 24-28 July 2017 at University of Birmingham, Birmingham, UK.

Contacts: Dr. Scott Piao (s.piao@lancaster.ac.uk), Dr. Paul Rayson (p.rayson@lancaster.ac.uk)
School of Computing and Communications
Lancaster University
Lancaster
UK
