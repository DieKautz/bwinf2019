package dev.diekautz.bwinf38.nummernmerker

import java.io.File

fun main(args: Array<String>) {
    if (args.isEmpty()) {

        File("src/dev/diekautz/bwinf38/nummernmerker/nummern.txt").forEachLine { //einlesen der nummern
            println(splitNumber(it))
        }
    } else {
        println(splitNumber(args[0]))
    }
}

fun splitNumber(num: String): SplitSolution {                    //aufteilen der nummern in blöcke
    if(num.length <= 4){
        return SplitSolution(arrayOf(num))
    } else {
        val len2 = splitNumber(num.substring(2, num.lastIndex))
        val len3 = splitNumber(num.substring(3, num.lastIndex))
        val len4 = splitNumber(num.substring(4, num.lastIndex))
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

class SplitSolution(val num: Array<String>) {              //prüfen das möglichst wenig 0 am anfang stehen
    fun getLeadingZeros(): Int {
        var count = 0
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

    fun prepend(string: String): SplitSolution {
        return SplitSolution(arrayOf(string) + num)
    }

    operator fun plus(other: SplitSolution): SplitSolution {
        return SplitSolution(num + other.num)
    }
}
