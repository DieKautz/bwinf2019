package dev.diekautz.bwinf38.blumenbeet

import java.io.File
import java.lang.Integer.max

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        for(i in 1..5){
            checkBestForFile("src/dev/diekautz/bwinf38/blumenbeet/blumen$i.txt")
            println("==============================================")
        }
    } else {
        checkBestForFile(args[0])
    }
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
        needColors.clear()
        for(wish in wishes.sortedByDescending { it.value }){
            if(needColors.size >= maxColors) break
            needColors.add(wish.first)
            if(needColors.size >= maxColors) break
            needColors.add(wish.second)
        }
    }
    println("Farben Anzahl: $needColors\nWünsche: $wishes")
    val bestBeet = generateHochbeet(Hochbeet(), maxColors, needColors, wishes)
    println("--------\n" +
            "Bester Score: ${bestBeet.getScore(wishes)}\n" +
            "Beet:\n$bestBeet"
    )
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

    fun nice(): String {
        return super.toString().padStart(7)
    }
}

class Wish(val first: Color, val second: Color, val value: Int){
    override fun toString(): String {
        return "($first:$second:${value}pkt)"
    }
}