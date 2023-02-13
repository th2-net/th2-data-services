#!/bin/bash
cd th2.data_services
perl -i -pe 's/^(#LOG )(.*)/$2 #LOG/' $(find . -type f)
