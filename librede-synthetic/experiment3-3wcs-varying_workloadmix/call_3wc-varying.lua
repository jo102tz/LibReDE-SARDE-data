--[[
	Gets called at the beginning of each "call cycle", perform as much work as possible here.
	Initialize all global variables here.
	Note that math.random is already initialized using a fixed seed (5) for reproducibility.
--]]
function onCycle()
	prefix = "http://10.1.234.186:8080/SyntheticComponents/"
end

--[[
	Gets called with ever increasing callnums for each http call until it returns nil.
	Once it returns nil, onCycle() is called again and callnum is reset to 1 (Lua convention).
	
	Here, you can use our HTML helper functions for conditional calls on returned texts (usually HTML, thus the name).
	We offer:
	- html.getMatches( regex )
		Returns all lines in the returned text stream that match a provided regex.
	- html.extractMatches( prefixRegex, postfixRegex )
		Returns all matches that are preceeded by a prefixRegex match and followed by a postfixRegex match.
		The regexes must one unique match for each line in which they apply.
	- html.extractMatches( prefixRegex, matchingRegex, postfixRegex )
		Variant of extractMatches with a matching regex defining the string that is to be extracted.
--]]
function onCall(callnum)
	branch = math.random(callnum)
	branch = branch % 3
	print(branch)
	if branch > 5000 then
		return prefix.. "wc1"
	elseif branch > 1000 then
		return prefix.. "wc2"
	else
		return prefix.. "wc3"
	end
end