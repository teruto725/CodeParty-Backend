#bin/bash
FILE=./main.py
URL=http://35.75.64.1:8080/codes/
INPUTNAME=file
curl -X POST -F file=@./main.py -H  "accept: application/json" -H  "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjI3MTQwMTY0LCJ1c2VyX2lkIjoxfQ.KW6wKhqrliBPsh0xBoHr2Qul2TR3Ot7jwuWrc6h9_LY"