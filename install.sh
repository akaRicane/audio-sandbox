npm install
python -m venv venv

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
pip install -r requirements.txt
echo "Packages installed ! Running sh.runserver.sh"
sh runserver.sh