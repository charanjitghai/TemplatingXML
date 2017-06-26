This repository aims at coming up with a template xml for n different xmls following same xsd.
Since XMLs don't have a concept of ordinality, comparing the ith element of first xml directly with ith element of second element doesn't make sense.
So, we first sort all the xmls, then check if any attribute values are different, if so, we generate tokens and token values for each of the differences for all the xmls, and generate the xml baselines, tokens accordingly.
