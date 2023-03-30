#!/bin/bash
# v 1.1.0

#find . -type f -exec sed -i.bak "s/th2_data_services/th2_data_services/g" {} \;
#sed 's/th2_data_services/th2_data_services/g' th2_data_services/utils/*



echo
date
echo
echo "Files for sed:"
echo "-------------------------------"
grep -Rc th2_data_services *
echo
echo "-------------------------------"
read -p 'Enter y to continue: ' agree

if [[ $agree == 'y' ]]; then
	grep -R th2_data_services * -l | xargs sed -i "s/th2_data_services/th2_data_services/g"
fi
