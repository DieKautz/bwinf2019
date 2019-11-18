local max_farben = {"blau", "gelb", "grün", "orange", "rosa", "rot", "türkis"}
local meine_farben = {}

local function table_copy(tbl)
	local newtbl = {}
	for key, value in pairs(tbl) do
		if type(value) == "table" then
			newtbl[key] = table_copy(value)
		else
			newtbl[key] = value
		end
	end
	return newtbl
end

local function table_search(tbl, search)
	for key, value in pairs(tbl) do
		if value == search then
			return key
		end
	end
	return -1
end

local function getVerfuegbareFarben()
	local farben = table_copy(max_farben)
	for key, value in pairs(meine_farben) do
		table.remove(farben, table_search(farben, value))
	end
	return farben
end

-- Farben einlesen
while true do
	print("Bitte verfügbare Farben eingeben (Auf Lager: ".. table.concat(getVerfuegbareFarben(), ",") ..") ODER C zum Bestätigen: ")
	local farbe = io.read()
	if farbe:lower() == "c" then
		print("")
		break
	elseif table_search(max_farben, farbe) == -1 then
		print("Diese Farbe ist leider nicht auf Lager")
	elseif table_search(meine_farben, farbe) ~= -1 then
		print("Diese Farbe haben Sie bereits ausgewählt")
	else
		table.insert(meine_farben, farbe)
	end
end

local function string_split(str, sep)
	if sep == nil then
		sep = "%s"
	end
	local tbl = {}
	for str in string.gmatch(str, "([^"..sep.."]+)") do
		table.insert(tbl, str)
	end
	return tbl
end

local meine_paare = {}

-- Paare einlesen
while true do
	print("Bitte Paar angeben, die Ihnen nebeneinander besonders gut gefallen (z.B. ".. meine_farben[1] .." ".. (meine_farben[2] or meine_farben[1]) .." 3) ODER C zum Bestätigen: ")
	local paar = io.read()
	paar = string_split(paar, " ")
	if paar[1]:lower() == "c" then
		print("")
		break
	elseif #paar ~= 3 then
		print("Falsche Eingabe!")
	elseif table_search(meine_farben, paar[1]) == -1 or table_search(meine_farben, paar[2]) == -1 then
		print("Diese Farbe haben Sie beim letzten Vorgang nicht ausgewählt")
	elseif paar[1] == paar[2] then
		print("Ein Paar muss unterschiedliche Farben haben")
	elseif not tonumber(paar[3]) or (tonumber(paar[3]) ~= 1 and tonumber(paar[3]) ~= 2 and tonumber(paar[3]) ~= 3) then
		print("Der Bonuspunkt muss eine gerade Zahl zwischen 1 bis 3 sein")
	else
		local updated = false
		for key, value in pairs(meine_paare) do
			if (value.farbe1 == paar[1] and value.farbe2 == paar[2]) or (value.farbe1 == paar[2] and value.farbe2 == paar[1]) then
				updated = true
				meine_paare[key].punkt = tonumber(paar[3])
			end
		end
		if not updated then
			table.insert(meine_paare, {farbe1 = paar[1], farbe2 = paar[2], punkt = tonumber(paar[3])})
		end
	end
end

local anzahlFarben = {}
local anzahlFarbenBisher = 0

for key, value in pairs(meine_farben) do
	anzahlFarbenBisher = anzahlFarbenBisher + math.floor(9 / #meine_farben)
	anzahlFarben[value] = math.floor(9 / #meine_farben)
end

while anzahlFarbenBisher < 9 do
	local farbeRandom = math.random(1, #meine_farben)
	local ran = math.random(0, 1)
	if ran >= 0.5 then
		anzahlFarbenBisher = anzahlFarbenBisher + 1
		anzahlFarben[meine_farben[farbeRandom]] = anzahlFarben[meine_farben[farbeRandom]] + 1
	end
end

local gKoord = {}

local function getKoord(x, y, koord)
	if x < 1 or x > 3 or y < 1 or y > 3 then
		return
	end
	if not koord then
		koord = gKoord
	end
	if koord[x] then
		return koord[x][y]
	end
end

local function setKoord(x, y, str, koord)
	if x < 1 or x > 3 or y < 1 or y > 3 then
		return
	end
	if not koord then
		koord = gKoord
	end
	if not koord[x] then
		koord[x] = {}
	end
	koord[x][y] = str
end

local x = 1
local y = 1

for key, value in pairs(anzahlFarben) do
	for i = 1, value do
		setKoord(x, y, key)
		x = x + 1
		if x > 3 then
			x = 1
			y = y + 1
		end
	end
end

local function displayKoord(koord)
	--[[
       ______________
      /            \
     /    türkis    \
    /                \
   /   türkis türkis  \
  /                    \
 | türkis türkis türkis |
  \                    /
   \   türkis türkis  /
    \                /
     \    türkis    /
      \            /
       ------------
	]]
	
	local function stretch(str)
		local missing = 6 - (str:find("ü") and str:len() - 1 or str:len())
		return string.rep(" ", math.ceil(missing / 2)) .. str .. string.rep(" ", math.floor(missing / 2))
	end
	
	local function colorize(color, str)
		color = color:gsub("ü", "ue")
		local colorCodes = {blau = 34, gelb = 33, gruen = 32, orange = 33, rosa = 35, rot = 31, tuerkis = 36}
		return "\27[".. colorCodes[color] .."m".. str .."\27[0m"
	end
	
	local function formatString(str)
		return colorize(str, stretch(str))
	end
	
	local str = "      ____________"
	str = str .."\n".."     /            \\"
	str = str .."\n".."    /    ".. formatString(getKoord(3, 1, koord)) .."    \\"
	str = str .."\n".."   /                \\"
	str = str .."\n".."  /   ".. formatString(getKoord(2, 1, koord)) .." ".. formatString(getKoord(3, 2, koord)) .."  \\"
	str = str .."\n".." /                    \\"
	str = str .."\n".."| ".. formatString(getKoord(1, 1, koord)) .." ".. formatString(getKoord(2, 2, koord)) .." ".. formatString(getKoord(3, 3, koord)) .." |"
	str = str .."\n".." \\                    /"
	str = str .."\n".."  \\   ".. formatString(getKoord(1, 2, koord)) .." ".. formatString(getKoord(2, 3, koord)) .."  /"
	str = str .."\n".."   \\                /"
	str = str .."\n".."    \\    ".. formatString(getKoord(1, 3, koord)) .."    /"
	str = str .."\n".."     \\            /"
	str = str .."\n".."      ------------"
	
	print("")
	
	print(str)
	
	-- Old output: Array like
	--[[
	local formatted = string.format("%%%ds | %%%ds | %%%ds", 5, 5, 5)
	for y = 1, 3 do
		print(string.format(formatted, stretch(getKoord(1, y, koord)), stretch(getKoord(2, y, koord)), stretch(getKoord(3, y, koord))))
		if y ~= 3 then
			print("------------------------")
		end
	end
	]]
	
	print("")
end

local function koordIterator()
	local x
	local y
	return function()
		if not x and not y then
			x = 1
			y = 1
		else
			x = x + 1
			if x > 3 then
				x = 1
				y = y + 1
				if y > 3 then
					x = nil
					y = nil
				end
			end
		end
		return x, y
	end
end

local function berechnePunkte(koord)
	local function berechne(x, y, eigeneFarbe, punkte)
		for key, value in pairs(meine_paare) do
			local nachbarFarbe = getKoord(x, y, koord)
			if not nachbarFarbe then
				break
			end
			if (value.farbe1 == eigeneFarbe and value.farbe2 == nachbarFarbe) or (value.farbe1 == nachbarFarbe and value.farbe2 == eigeneFarbe) then
				punkte = punkte + value.punkt
			end
		end
		return punkte
	end
	
	local punkte = 0
	for x, y in koordIterator() do
		local eigeneFarbe = getKoord(x, y, koord)
		punkte = berechne(x + 1, y, eigeneFarbe, punkte)
		punkte = berechne(x + 1, y + 1, eigeneFarbe, punkte)
		punkte = berechne(x, y + 1, eigeneFarbe, punkte)
	end
	return punkte
end

local function sortKoord()
	for x, y in koordIterator() do
		local eigeneFarbe = getKoord(x, y)
		for x2, y2 in koordIterator() do
			local copiedKoord = table_copy(gKoord)
			local tauschFarbe = getKoord(x2, y2)
			setKoord(x, y, tauschFarbe, copiedKoord)
			setKoord(x2, y2, eigeneFarbe, copiedKoord)
			if berechnePunkte(copiedKoord) > berechnePunkte() then
				gKoord = copiedKoord
				return sortKoord()
			end
		end
	end
end


sortKoord()

displayKoord()
print("Bonuspunkte: ".. berechnePunkte())
