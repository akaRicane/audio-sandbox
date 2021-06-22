npm install
# TODO code may won't work if python path link to python version not supported
# User should specify version


if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        python3 -m venv venv
        source venv/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
        python3 -m venv venv
        source venv/bin/activate
elif [[ "$OSTYPE" == "msys"* ]] ; then
        python -m venv venv
        source venv/Scripts/activate
else
    echo "Install failed !! Ask Pascal"

fi
echo "Install is a success ! Processing packages ..."

if [[ "$OSTYPE" == "msys"* ]]; then
        python -m pip install wheel
        python -m pip install -r requirements.txt
        python -m pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl

else
        python3 -m pip install wheel
        python3 -m pip install -r requirements.txt
        python3 -m pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
fi
echo "Packages installed ! Please run: sh.runserver.sh"