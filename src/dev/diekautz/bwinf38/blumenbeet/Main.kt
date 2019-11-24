package dev.diekautz.bwinf38.blumenbeet

import java.io.File
import java.lang.Integer.max

fun main() {
//    for(i in 1..5){
//        checkBestForFile("src/dev/diekautz/bwinf38/blumenbeet/blumen$i.txt")
//        println("==============================================")
//    }
    checkBestForFile("src/dev/diekautz/bwinf38/blumenbeet/blumen1.txt")
}

fun checkBestForFile(path: String){
    val file = File(path).readLines()
    val maxColors = file[0].toInt()
    val wishCount = file[1].toInt()

    val wishes =  mutableSetOf<Wish>()
    val needColors = mutableSetOf<Color>()
    for(i in 0.until(wishCount)){
        //file[2+i]
        val s = file[2+i].split(" ")
        val color1 = Color.valueOf(s[0].toUpperCase())
        val color2 = Color.valueOf(s[1].toUpperCase())
        val value = s[2].toInt()
        wishes.add(Wish(color1, color2, value))
        needColors.add(color1)
        needColors.add(color2)
    }
    if(maxColors < needColors.size){
        println("\u001B[1;31mFEHLER: Die Anzahl der verschiedenen Farben ist kleiner als die der Lieblingsfarben.")
        return
    }
    println(generateHochbeet(Hochbeet(), maxColors, needColors, wishes))
}

fun generateHochbeet(beet: Hochbeet, maxColors: Int, needColors: MutableSet<Color>, wishes: MutableSet<Wish>): Hochbeet {
    if(beet.flowers.size >= 9){
        return beet
    }
    var bestScore = -1
    var bestBeet = Hochbeet()
    for(i in 0 until maxColors){
        val color = if(i < needColors.size){
            needColors.elementAt(i)
        } else {
            Color.values().subtract(needColors).elementAt(i-needColors.size)
        }
        val testBeet = Hochbeet(beet.flowers)
        testBeet.flowers.add(color)
        val generated = generateHochbeet(testBeet, maxColors, needColors, wishes)
        val score = generated.getScore(wishes)
        if(score >= bestScore){
            bestScore = score
            bestBeet = generated
        }
    }
    return bestBeet
}

class Hochbeet(default: ArrayList<Color>) {
    val flowers = ArrayList<Color>(default)

    constructor() : this(arrayListOf())

    fun getScore(wishes: MutableSet<Wish>): Int {
        var value = 0

        if(!wishes.all { flowers.contains(it.first) && flowers.contains(it.second) }){
            return -1
        }

        CONNECTED.forEach { ot ->
            if(flowers.size-1 >= max(ot[0].toInt()-48, ot[0].toInt()-48)){ //wenn beet schon weit genug bestückt
                val first = flowers[ot[0].toInt() - 48]
                val second = flowers[ot[1].toInt() - 48]
                wishes.forEach {
                    if ((it.first == first && it.second == second) || (it.first == second && it.second == first)) {
                        //println("${it.first}[${ot[0]}] - ${it.second}[${ot[1]}]\t-> +${it.value} Pkt.")
                        value += it.value
                    }
                }
            }
        }

        return value
    }

    override fun toString(): String {
        return "\t\t${flowers[0]}\n" +
                "\t${flowers[1]} ${flowers[2]}\n" +
                "${flowers[3]} ${flowers[4]} ${flowers[5]}\n" +
                "\t${flowers[6]} ${flowers[7]}\n" +
                "\t\t${flowers[8]}\n"
    }

    companion object {
        val CONNECTED = arrayOf("01", "02",
            "12", "13", "14", "24", "25",
            "34", "36", "45", "46", "47", "57",
            "67", "68", "78")
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
}

class Wish(val first: Color, val second: Color, val value: Int){
    override fun toString(): String {
        return "($first:$second:${value}pkt)"
    }
}