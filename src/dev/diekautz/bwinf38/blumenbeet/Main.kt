package dev.diekautz.bwinf38.blumenbeet

import java.io.File
import java.lang.Integer.max

fun main(args: Array<String>) {
    //Wenn ein Argument vorhand -> als Pfad für Datei nutzen
//    if (args.isEmpty()) {
//        for(i in 1..5){
//            checkBestForFile("src/dev/diekautz/bwinf38/blumenbeet/blumen$i.txt")
//            println("==============================================")
//        }
//    } else {
//        checkBestForFile(args[0])
//    }
    checkBestForFile("src/dev/diekautz/bwinf38/blumenbeet/blumen1.txt")
}

/**
 * Gibt das bestmögliche Hochbeet für eine Eingabe zurück
 *
 * @param path Pfad zur Eingabedatei
 */
fun checkBestForFile(path: String){
    val file = File(path).readLines()
    val maxColors = file[0].toInt()//maximale Anzahl auf erster Zeile
    val wishCount = file[1].toInt()//Anzahl der Wünsche auf zweiter Zeile

    val wishes =  mutableSetOf<Wish>()
    val needColors = mutableSetOf<Color>()
    for(i in 0.until(wishCount)){//Einlesen der einzelnen Wünsche
        //file[2+i]
        val s = file[2+i].split(" ")
        val color1 = Color.valueOf(s[0].toUpperCase())
        val color2 = Color.valueOf(s[1].toUpperCase())
        val value = s[2].toInt()
        wishes.add(Wish(color1, color2, value))//Hinzufügen zum Set
        needColors.add(color1)//Hinzufügen der ersten Farbe zu den Benötigten
        needColors.add(color2)//Hinzufügen der zweiten Farbe zu den Benötigten
    }
    if(maxColors < needColors.size){//Wenn mehr Farben in Wünschen erwähnt muss gefiltert werden
        needColors.clear()
        for(wish in wishes.sortedByDescending { it.value }){//Ordnen der Wünsche nach Wert
            if(needColors.size >= maxColors) break//Hinzufügen einer weiteren Farbe nur wenn noch nicht zu viel
            needColors.add(wish.first)
            if(needColors.size >= maxColors) break
            needColors.add(wish.second)
        }
    }
    println("maxColors: $maxColors\nneededColors: $needColors\nWünsche: $wishes")
    val bestBeet = generateHochbeet(Hochbeet(), maxColors, needColors, wishes)//Aufruf der rekursiven Funktion

    //Ausgabe
    println("--------\n" +
            "Bester Score: ${bestBeet.getScore(wishes, needColors)}\n" +
            "Beet:\n$bestBeet"
    )
}

/**
 * Gibt das bestmögliche Hochbeet zurück
 * @param beet Startbeet für den rekursiven Aufruf
 * @param maxColors maximale Anzahl an verschiedenen Farben
 * @param needColors Farben die unbedingt benötigt werden
 * @param wishes Wünsche nach denen bewertet wird
 *
 * @return bestmögliche Hochbeet aus den Wünschen
 */
fun generateHochbeet(beet: Hochbeet, maxColors: Int, needColors: MutableSet<Color>, wishes: MutableSet<Wish>): Hochbeet {
    if(beet.flowers.size >= 9){//Abbruchbedigung, da rekursiver Aufruf
        return beet
    }

    var bestScore = -1
    var bestBeet = Hochbeet()
    for(i in 0 until maxColors){//Ausprobieren jeder möglichen Farbe
        val color = if(i < needColors.size){
            needColors.elementAt(i)
        } else {
            Color.values().subtract(needColors).elementAt(i-needColors.size)
        }
        if(beet.flowers.contains(color)){
            if(beet.flowers.subtract(needColors).size + needColors.size < maxColors){
                continue
            }
        }
        val testBeet = Hochbeet(beet.flowers)
        testBeet.flowers.add(color)//Erzeugung eines "Testbeetes"
        val generated = generateHochbeet(testBeet, maxColors, needColors, wishes)
        val score = generated.getScore(wishes, needColors)
        if(score >= bestScore){//Bewertung des Beetes und Vergleich mit Bestem
            bestScore = score
            bestBeet = generated
        }
    }
    return bestBeet
}

class Hochbeet(default: ArrayList<Color>) {
    /**Anordnung der Farben als Array wie folgt:
     *    0
     *   1 2
     *  3 4 5
     *   6 7
     *    8
    **/
    val flowers = ArrayList<Color>(default)

    constructor() : this(arrayListOf())

    /**
     * Berechnet die Punktzahl eines Hochbeets
     *
     * @param wishes Wünsche für die Bewertung
     * @return die Punktzahl
     */
    fun getScore(wishes: MutableSet<Wish>, needColors: MutableSet<Color>): Int {
        var value = 0

        if(!needColors.all { flowers.contains(it) }){//Wenn nicht alle nötigen Farben verwendet dann unbrauchbar
            return -1
        }

        CONNECTED.forEach { ot ->
            if(flowers.size-1 >= max(ot[0].toInt()-48, ot[0].toInt()-48)){ //wenn Beet schon weit genug bestückt
                val first = flowers[ot[0].toInt() - 48]
                val second = flowers[ot[1].toInt() - 48]
                wishes.forEach {
                    if ((it.first == first && it.second == second) || (it.first == second && it.second == first)) {
                        value += it.value //für jedes angrenzende Paar aus Wunsch wird Punktzahl addiert
                    }
                }
            }
        }

        return value
    }

    override fun toString(): String {
        return "\t\t${flowers[0].nice()}\n" +
                "\t${flowers[1].nice()} ${flowers[2].nice()}\n" +
                "${flowers[3].nice()} ${flowers[4].nice()} ${flowers[5].nice()}\n" +
                "\t${flowers[6].nice()} ${flowers[7].nice()}\n" +
                "\t\t${flowers[8].nice()}\n"
    }

    companion object {
        val CONNECTED = arrayOf("01", "02",
            "12", "13", "14", "24", "25",
            "34", "36", "45", "46", "47", "57",
            "67", "68", "78") //Angrenzende Beete in der Konstellation
    }
}

enum class Color {
    BLAU,
    GELB,
    GRUEN,
    ORANGE,
    ROSA,
    ROT,
    TUERKIS;

    fun nice(): String {
        return super.toString().padStart(7)
    }
}

class Wish(val first: Color, val second: Color, val value: Int){
    override fun toString(): String {
        return "($first:$second:${value}pkt)"
    }
}