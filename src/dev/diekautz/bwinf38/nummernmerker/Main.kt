

package dev.diekautz.bwinf38.nummernmerker
 
import java.io.File
 
fun main() {
    File("src/dev/diekautz/bwinf38/nummernmerker/nummern.txt").forEachLine { //einlesen der nummern
        println(splitNumber(it)) //Für jede Zeile(Nummer) Lösung eingeben
    }
}
 
fun splitNumber(num: String): SplitSolution {
    if(num.length <= 4){ //Wenn ein Block kleiner als 4 ist kann er nicht zerlegt werden (bei 4 macht es keinen Sinn)
        return SplitSolution(arrayOf(num))
    } else {
        val len2 = splitNumber(num.substring(2, num.lastIndex)) //testen mit einem zweierblock
        val len3 = splitNumber(num.substring(3, num.lastIndex)) //testen mit einem dreierblock
        val len4 = splitNumber(num.substring(4, num.lastIndex)) //testen mit einem viererblock
 
		//vergleichen bei welcher Aufteilung am kleinsten und dann mit dieser weiter arbeiten
        if(len2.getLeadingZeros() < len3.getLeadingZeros()){
            if (len2.getLeadingZeros() < len4.getLeadingZeros()){
                return len2.prepend(num.substring(0, 2))
            } else {
                return len4.prepend(num.substring(0, 4))
            }
        } else {
            if(len3.getLeadingZeros() < len4.getLeadingZeros()){
                return len3.prepend(num.substring(0, 3))
            } else {
                return len4.prepend(num.substring(0, 4))
            }
        }
    }
}
 
class SplitSolution(val num: Array<String>) {
    fun getLeadingZeros(): Int {
        var count = 0
		//Für jeden Block der mit "0" beginnt wird die Anzahl um 1 erhöht
        num.forEach {
            if(it.startsWith("0")){
                count++
            }
        }
        return count
    }
 
    override fun toString(): String {
        return num.joinToString(" ")
    }
 
    fun prepend(string: String): SplitSolution { //Hilfsfunktion zum Anfügen von zeichen am Anfang
        return SplitSolution(arrayOf(string) + num)
    }
 
    operator fun plus(other: SplitSolution): SplitSolution { //Hilfsfunktion um zwei Aufteilungen zusammen zu setzten
        return SplitSolution(num + other.num)
    }
}
