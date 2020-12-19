# Blender addon: Creator Music Visualization

# Language: English
## Basic information
- Addon version: 1.0.0
- Blender version: 2.91.0
- Location: ' View3D > UI '

## Description
'Creator Music Visualization' is a simple tool that allows the user to generate a visualization for selected music in MP3 format.
Works only on the Windows version of the Blender.

## Addon instalation
1. After starting the Blender, go to 'Edit' and select 'Preferences'.
2. In 'Preferences' we select the 'Add-ons' tab
3. Select the "Install" button and we find the file "VMAddony.py".
4. after installing the file, select addon 'Tools: Creator Music Visualization' as active

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_install_addon_shortcut.png?raw=true)

## Features in the Blender UI
1. The first two fields allow you to specify the location of the MP3 file to be loaded and the place to save our visualization.
2. The third field is used to import a 'COWM.obj' file with an object for visualization. It is necessary to generate the visualization. The 'COWM.obj' file is located in the folder with the 'VMAddony.py' file.
3. The fourth field allows you to name the video file.
4. The three further options allow you to modify elements occurring in the visualization by changing colors.
5. The other options allow you to specify video resolution, quality and frame rate. In case the user knows what is the sampling rate of the MP3 file can change it.
6. After pressing the 'RENDER VISUALIZATION' button, a console appears, which is used to inform about the current state of preparation for rendering and the progress of visualization generation. Generation duration depends on the equipment, length of music (I recommend songs longer or equal to 1 minute) and selected parameters by the user.

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_UI_Shorcut.png?raw=true)
![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_console.PNG?raw=true)

## Description visualization
The visualization of music created by the addon consists of the object that has the form of a three-dimensional sphere with four particle emitters. Each emitter supports one of the four frequency ranges: 0-250Hz, 250-500Hz, 500-750Hz, 750-1000Hz. The ball rotates in one axis and at the same time gently swings in the other axis. At the same time, it releases particles that fade or glow and become smaller/bigger by the sounds of music. Also the colors on the object change under the influence of music.

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_MV.PNG?raw=true)

In the middle of the music there is a change in the direction of the ball's rotation and mirrors appear

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blende_MV2.PNG?raw=true)

The visualization also has an ending and changes in the camera position. 


# Language: Polish
## Podstawowe informacje
- Wersja addona: 1.0.0
- Wersja Blendera: 2.91.0
- Lokalizacja: ' View3D > UI '

## Opis
'Creator Music Visualization' jest prostym narzędziem, który pozwala użytkownikowi wygenerowanie wizualizacji do wybranej muzyki w formacie MP3.
Działa tylko na Blenderze w wersji na systemy Windows.

## Instalacja addona
1. Po uruchomieniu Blendera wchodzimy do 'Edit' i wybieramy opcje 'Preferences'
2. W 'Preferences' wybieramy zakładkę 'Add-ons'
3. Wybieramy przycisk 'Install' i szukamy plik 'VMAddony.py'
4. Po zainstalowaniu pliku zaznaczamy addon 'Tools: Creator Music Visualization' jako aktywny

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_install_addon_shortcut.png?raw=true)

## Funkcje w Blender UI
1. Pierwsze dwa pola umożliwiają podanie lokalizacji pliku MP3 do załadowania oraz miejsce do zapisu naszej wizualizacji.
2. Trzecie pole to służy do zaimportowania pliku 'COWM.obj' z obiektem do wizualizacji. Jest on konieczny do wygenerowania wizualizacji. Plik 'COWM.obj' znajduję się w folderze z plikiem 'VMAddony.py'.
3. Czwarte pole umożliwia nadanie nazwy pliku wideo.
4. Trzy kolejne opcje pozwalają na modyfikacje elementów występujących w wizualizacji po przez zmianę kolorów.
5. Pozostałe opcje umożliwiają podanie rozdzielczości wideo, jakość i liczbę klatek na sekundę. Przypadku, gdy użytkownik wie jaka jest częstotliwość próbkowania pliku MP3 może ją zmienić.
6. Po wciśnięciu przycisku 'RENDER VISUALIZATION' pojawia się konsola, która służy do informowania o obecnym stanie przygotowania do renderingu i postępach generowania wizualizacji. Czas trwania generowania zależy od sprzętu, długości muzyki (zalecam dłuższe bądź równe 1 minutę utwory) oraz wybranych parametrów przez użytkownika

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_UI_Shorcut.png?raw=true)
![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_console.PNG?raw=true)

## Opis wizualizacji
Wizualizacja muzyki powstała dzięki addonowi składa się z obiektu, która ma postać trójwymiarowej kuli z czterema emiterami cząstek. Każdy emiter obsługuje jeden z czterech zakresów częstotliwości: 0-250Hz, 250-500Hz, 500-750Hz, 750-1000Hz. Kula obraca się w jednej osi i równocześnie delikatnie się wychyla w drugiej osi. W tym sam czasie wypuszcza cząstki, które gasną/zapają się oraz zmiejszają się/zwiększają się pod wpływem dźwięków z muzyki. Również kolory na obiekcie ulegają zmianą pod wpływem muzyki.

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blender_MV.PNG?raw=true)

W połowie muzyki następuje twist w postaci pojawienia się luster. Dodatkowo obiekt zmienia kierunek obrotu w drugą stronę.

![alt text](https://github.com/PolskiPiter/Blender_Addon_Music_Visualization/blob/main/Images/Blende_MV2.PNG?raw=true)

Wizualizacja posiada także zakończenie i zmiany w położeniu kamery. 
