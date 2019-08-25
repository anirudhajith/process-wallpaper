#!/bin/bash
if [[ "$OSTYPE" =~ ^msys ]]; then
    ## Fixes the installer on Bash for Windows
    alias python3='py -3'
    echo "Checking Python dependencies..."
    pillow="$(py -3 -c 'import pkgutil; print(1 if pkgutil.find_loader("PIL") else 0)')"
    wordcloud="$(py -3 -c 'import pkgutil; print(1 if pkgutil.find_loader("wordcloud") else 0)')"
    matplotlib="$(py -3 -c 'import pkgutil; print(1 if pkgutil.find_loader("matplotlib") else 0)')"
    psutil="$(py -3 -c 'import pkgutil; print(1 if pkgutil.find_loader("psutil") else 0)')"
else
    echo "Checking Python dependencies..."
    pillow="$(python3 -c 'import pkgutil; print(1 if pkgutil.find_loader("PIL") else 0)')"
    wordcloud="$(python3 -c 'import pkgutil; print(1 if pkgutil.find_loader("wordcloud") else 0)')"
    matplotlib="$(python3 -c 'import pkgutil; print(1 if pkgutil.find_loader("matplotlib") else 0)')"
    psutil="$(python3 -c 'import pkgutil; print(1 if pkgutil.find_loader("psutil") else 0)')"
fi

if [[ $pillow == 0 ]]; then
    echo "Installing Pillow..."
    pip3 install --user Pillow
fi
if [[ $wordcloud == 0 ]]; then
    echo "Installing wordcloud..."
    pip3 install --user wordcloud
fi
if [[ $matplotlib == 0 ]]; then
    echo "Installing matplotlib..."
    pip3 install --user matplotlib
fi
if [[ $psutil == 0 ]]; then
    echo "Installing psutil..."
    pip3 install --user psutil
fi

echo "Creating wallpaper..."
sh updateWallpaper.sh

echo "Setting wallpaper..."
sh setWallpaper.sh

echo "Setup successfully completed"
