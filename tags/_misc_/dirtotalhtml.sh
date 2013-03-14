#!/bin/sh
# Count dir sizes and their files
echo "<html>
<head>
  <meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">
  <title> Index </title>
 </head>
 <body>
  <table border=\"1\">
   <thead>
    <tr> <th> Dir </th> <th> Size (MB) </th> <th> Files </th> </tr>
   </thead>
"

ls -1 | while read i
do
    #echo "$i"
    if [ -d "$i" ]; then
        DU=`du -sm "$i" | gawk '{print $1}'`
        QTY=`find "$i" -type f | wc -l`
        echo "    <tr> <td> $i </td> <td align=\"right\"> $DU </td> <td align=\"right\"> $QTY </td> </tr>"
    fi
done
echo "  </table>
 </body>
</html>"
