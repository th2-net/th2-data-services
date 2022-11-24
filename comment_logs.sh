#!/bin/bash
cd th2_data_services
perl -i -pe 's/(.*)( #LOG)$/#LOG $1/' $(find . -type f)
