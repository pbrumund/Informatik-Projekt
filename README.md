# Informatik-Projekt
# Projekt: Pyano

Bei dem Projekt handelt es sich um ein Tastenfeld, welches am Arduino angeschlossen ist und mit dem
am Computer Tastenkombinationen ausgeführt oder Texte/Wörter eingegeben werden können. Dazu
wird der Knopfdruck vom Arduino an den Computer gesendet, der den zu der Taste gehörenden Befehl
ausführt. Dieser simuliert mittels der Bibliothek „Pyautogui“ eine Tastatureingabe.

## Anschluss und Installation
An dem Arduino ist an den Pins 4-7 und 10-13 ein Tastenfeld im 4*4-Layout angeschlossen. Der
Arduino ist außerdem über ein WLAN-Shield mit dem Computer verbunden und wird über eine
passende Quelle mit Strom versorgt.

Zur Installation werden für Python die Bibliotheken Pyautogui, Tkinter, Socket und JSON benötigt.
Der Arduino benötigt die Dumb-Server-Bibliothek und die Keypad-Bibliothek (https://playground.arduino.cc/Code/Keypad) (Beide im selben Ordner
wie die Arduino-Datei). Auf dem Arduino läuft das „Keypad_Arduino“-Programm, auf dem Computer
„Keypad_GUI“.

Die Pyautogui-Bibliothek wurde an das deutsche Tastaturlayout angepasst, wobei nur die Windows-
spezifische Datei angepasst wurde. Daher können bestimmte Sonderzeichen und Umlaute nur über
Windows eingegeben werden. Zur Installation müssen aus der offiziellen Version (https://github.com/asweigart/pyautogui) die \_\_init__- und die
_pyautogui-win-Datei ersetzt werden.

## Verbinden mit dem Computer
Um den Computer mit dem als Server arbeitenden Arduino zu verbinden werden die über USB
übermittelte IP-Adresse und der Port des Arduinos in ein dazu gedachtes Fenster eingegeben. Dieses
wird bei dem Start des Programms oder bei Verlust der Verbindung geöffnet. Beim Klick auf „Connect“
wird versucht, eine Verbindung einzugehen und das Fenster schließt sich.

## Bedienung des Programms
Im Hauptfenster werden die Buttons des Tastenfelds in derselben Konfiguration angezeigt, in der sie
auf dem Tastenfeld beschriftet sind. Um den zugewiesenen Text bzw. Befehl zu ändern, wird ein Button
im Fenster angeklickt. Dieser wird nun zum Bearbeiten ausgewählt und farblich markiert. Im darunter
liegenden Textfeld und der daneben liegenden Checkbox wird nun die aktuelle Tastenbelegung
angezeigt. Der neue Text kann nun eingegeben werden und über die Checkbox kann ausgewählt
werden, ob der Text als Tastenkombination ausgeführt werden soll. Eine Tastenkombination wird
eingegeben, indem die einzelnen Bezeichnungen der Tasten mit Leerzeichen getrennt eingegeben
werden (z.B. „ctrl shift esc“ oder „win e“) Durch einen Klick auf „Speichern“ wird die neue Belegung
gespeichert und überschreibt die alte.

Um die gesamte Konfiguration zu speichern, wird auf „Profil speichern“ geklickt. Daraufhin öffnet
sich ein Dateiexplorer, in dem der Speicherordner ausgewählt und ein Dateiname eingegeben werden
muss. Die Datei wird im JSON-Format gespeichert, wobei die Dateiendung nicht mit eingegeben wird.
Durch einen Klick auf „Profil laden“ kann ein zuvor erstelltes Profil geladen werden, wodurch häufig
benutzte Konfigurationen nicht jedes mal neu eingeben zu müssen. Es öffnet sich ebenfalls ein
Dateiexplorer, in dem das gewünschte Profil ausgewählt werden kann. Falls der Dateiexplorer
geschlossen wird ohne eine Datei auszuwählen bzw. einen Dateinamen einzugeben, wird der Lade-
bzw. Speichervorgang abgebrochen.

Um den gespeicherten Befehl auszuführen muss der entsprechende Knopf des am Arduino
angeschlossenen Tastenfeldes gedrückt werden. Dieser befindet sich an der gleichen Stelle und hat die
gleiche Beschriftung wie der am Computer angezeigte Button. Wird ein Knopf auf dem Tastenfeld
gedrückt, übermittelt der Arduino die Nummer des Buttons (nicht die Beschriftung). Python empfängt
diese und führt den gewünschten Befehl aus. Dazu wird entweder der eingegebene String über
Pyautogui eingegeben oder falls der Button mit einer Tastenkombination belegt ist, diese ausgeführt.

Beim Schließen des Fensters wird ein Befehl an den Arduino gesendet, um diesen neu zu starten. Daher
dauert es ca. eine Sekunde, um das Fenster zu schließen.
