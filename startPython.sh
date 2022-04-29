#!/bin/bash

clear
echo -e " PimpMySuperWatt python direct installation\n"
echo -e " Check prequisites... \n\n"
echo -e " - Checking python version need 3.7 : \c"
VERSION=$(test -f /usr/local/bin/python3.7 && echo 1)
if [ "${VERSION}" != "1" ]
 then
  echo "KO $(python -V 2>&1)"
  echo -e "   --> Can't find /usr/local/bin/python3.7\n"
  echo -e "       check install"
  exit 1
fi

echo -e " - Cleaning .venv python : \c"
rm -rf .venv 2>/dev/null
if [ "$?" -eq 0 ]
 then
  echo "OK"
 else
  echo "FAIL can't delete .venv directory \n" ; exit 1
fi
echo -e " - Creating .venv python : \c"
/usr/local/bin/python3.7 -m venv .venv
if [ "$?" -eq 0 ]
 then
  echo "OK"
 else
  echo -e "Can't create .venv , try manually /usr/bin/python3.7 -m venv .venv\n\n" ; exit 1
fi

echo -e " - Installing dependencies : "
for DEP in $(cat ./python/requirements.txt)
 do
  echo -e "   * $DEP : \c"
  .venv/bin/pip3 install $DEP >/dev/null 2>&1
  if [ "$?" -eq 0 ]
   then
     echo "OK"
   else
     echo "FAIL for .venv/bin/pip3 install $DEP"
  fi
 done

echo -e " - Starting PimpMySuperwatt"
.venv/bin/python3 ./python/superwatt.py --debug ./python/superwatt.json
