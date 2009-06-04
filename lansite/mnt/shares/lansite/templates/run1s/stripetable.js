function makeStripe(tab)
{
	var rows = tab.getElementsByTagName("tr");

	if (!rows)
		return;

	for(var i=0; i<rows.length; i++)
		rows[i].className = ((i%2)==0 ? "odd" : "even");
}