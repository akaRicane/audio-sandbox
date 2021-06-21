npm install
# TODO code may won't work if python path link to python version not supported
# User should specify version
python3 -m venv venv

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        source venv/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
elif [[ "$OSTYPE" == "msys"* ]] ; then
        source venv/Scripts/activate
else
    echo "Install failed !! Ask Pascal"

fi
echo "Install is a success ! Processing packages ..."
python3 -m pip install wheel
python3 -m pip install -r requirements.txt
python3 -m pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
echo "Packages installed ! Please run: sh.runserver.sh"