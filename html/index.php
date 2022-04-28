<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>

    <title>
      GM4SLV DSC Logs 
    </title>
<meta http-equiv="refresh" content="300">
<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1">
<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
<style>
#mid{
color: white;
background: #006666;
width:70px;
height:30px;
border-radius: 10px;
cursor: pointer;
}
 #freq{
color: white;
background: #006666;
width:70px;
height:30px;
border-radius: 10px;
cursor: pointer;
}
 #rx {
color: white;
background: #6666cc;
width:160px;
height:30px;
border-radius: 10px;
cursor: pointer;
}
 #rx_small {
color: white;
background: #6666cc;
width:160px;
height:30px;
font-size:70%;
border-radius: 10px;
cursor: pointer;
}
#link {
color: white;
background: #6699cc;
width:160px;
height:30px;
border-radius: 10px;
cursor: pointer;
}
#dis {
color: #ffffff;
background: #a0a0cd;
width:160px;
height:30px;
border-radius: 10px;
cursor: pointer;
}
inputtype=submit{
color: white;
background: #003366;
width:60px;
height:30px;
border-radius: 10px;

}

</style>
<basefont face="Arial">

	  </head>
<body bgcolor="c8d5e6">
	
<center>

<h1><font color=#006666>
Multi-Receiver Multi-Band MF/HF DSC Monitoring
</font>
</h1>

<!--<iframe frameborder=0 align=top marginheight=0 scrolling=auto width=40%  src="./pages/php/rx_online.php" ></iframe>-->
<hr width=50%>



<h2><font color=#006666>DSC Messages</h2></font>

<b>Today's messages</b><br>
<br>
Each band covers a 2MHz bandwidth, to include the normal GMDSS channels and any other DSC channels.<br>
To check for messages on unusual frequencies, tick the "Ignore GMDSS Channels" box.
<br><br>
<form action="./pages/php/band_today.php" method="GET">
<!--<table cellpadding=5>
<tr>

<td><input type="checkbox" name="ecc" value="all" />Include messages with<br>checksum failure (ECC=ERR)?</td>
<td>
<input type="checkbox" name="tilde" value="y" checked />Ignore incomplete messages with<br>symbol parity failures?</td>

<td>

<input type="checkbox" name="ignore" value="y" />Ignore GMDSS Channels</td></tr>


</table>
-->
<input type="checkbox" name="ignore" value="y" />Ignore GMDSS Channels</td></tr>

<input type="checkbox" name="notest" value="y" />Ignore Test Messages
<input type="checkbox" name="urgdis" value="y" />Only Urgency/Distress
 
<br>
<br>
<table><caption><b>Time range</b></caption>
<tr>
<td>
<input type="radio" name="timescale" value="1" checked />1 hours
</td>
<td>
<input type="radio" name="timescale" value="6"  />6 hours
</td>
<td>
<input type="radio" name="timescale" value="12" />12 hours
</td>
<td>
<input type="radio" name="timescale" value="24" />24 hours
</td>
</tr>
</table>

<br>
<table><caption><b>Message Sender filter</b></caption>
<tr>
<td>
<input type="radio" name="coast" value="coast" />Coast
<input type="radio" name="coast" value="ship" />Ship
<input type="radio" name="coast" value="cc" /> Coast to Coast
<input type="radio" name="coast" value="ss" />Ship to Ship
<input type="radio" name="coast" value="%"checked  />All</td>
</tr>
</table>
<br>
<table cellpadding=5>
<tr>
<td><input id="freq" type="submit" name="rx_freq" value="2" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="4" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="6" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="8" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="12" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="16" /> MHz band</td>
</tr>
</table>
<table>
<tr>
<tr><td><center>All bands 2MHz - 30MHz :   <input id="freq" type="submit" name="rx_freq" value="ALL" /></center></td>
<!--<td><input id="freq" type="submit" name="rx_freq" value="18" /> MHz band</td>-->
 
</tr>
</table>
</form>
<hr width=30%>
<!--
<h4>DSC Messages showing one copy of each message received</h4>
Messages from the last 60 minutes.
<form action="./pages/php/nodup.php" method="GET">
<table cellpadding=5>
<tr>
<td><input id="freq" type="submit" name="rx_freq" value="2187.5" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="4207.5" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="6312.0" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="8414.5" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="12577.0" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="16804.5" /></td>
</tr>
</table>
<table>
<tr>
<td><center>All bands 2MHz - 30MHz :   <input id="freq" type="submit" name="rx_freq" value="ALL" /></center></td>
</tr>
</table>
</form>
<hr width=30%>
-->
<table cellpadding=5, rules=cols>
<tr>
<th><b>Coast Station Traffic by Continent / [MID] </b></th>
<th><b>Ship Station Traffic by Continent / [MID]</b></th>
</tr>


<tr>
<td>
<form action="./pages/php/mid_today.php" method="GET">
<input type="checkbox" name="notest" value="y" />Ignore Test Messages
<input type="checkbox" name="urgdis" value="y" />Only Urgency/Distress


    <table cellpadding=5>
    <tr>
    <td><center><input id="freq" type="submit" name="mid" value="[200]" /><br>Europe/Russia</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[300]" /><br>N.America/Caribbean</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[400]" /><br>Asia/Middle East</center></td>
    </tr>
    <tr>
    <td><center><input id="freq" type="submit" name="mid" value="[500]" /><br>Australasia/S.E. Asia</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[600]" /><br>Africa</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[700]" /><br>S. America</center></td>
    </tr>
    </table>    
</form>
</td>

<td>
<form action="./pages/php/ship_mid_today.php" method="GET">
<input type="checkbox" name="notest" value="y" />Ignore Test Messages
<input type="checkbox" name="urgdis" value="y" />Only Urgency/Distress



    <table cellpadding=5>
    <tr>
    <td><center><input id="freq" type="submit" name="mid" value="[200]" /><br>Europe/Russia</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[300]" /><br>N.America/Caribbean</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[400]" /><br>Asia/Middle East</center></td>
    </tr>
    <tr>
    <td><center><input id="freq" type="submit" name="mid" value="[500]" /><br>Australasia/S.E. Asia</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[600]" /><br>Africa</center></td>
    <td><center><input id="freq" type="submit" name="mid" value="[700]" /><br>S. America</center></td>
    </tr>
    </table>
</form>
</td>

</tr>
</table>

<!--
<hr width = "30%">
<b>Select Messages based on Vessel Class</b><br><br>
<form action="./pages/ship_types.html">
<input id="link" type="submit" value="Vessel Class">
</form><br>
-->

<hr width = "80%">
<h2><font color=#006666>Other Functions</h2></font>

<table cellpadding=5 rules="cols">
<th>Search</th>
<th>REU / RWW</th>
<!--<th>Create a list of each Coast<br> Station heard by any<br>network member, Band by Band</th>-->
<th>
Active Receivers
</th>
<th></th>
<!--<th>Graphs of message arrival rates</th>-->

<tr>
<td><center>
Search current database<br>
<font size="2pt">
30 October 2017 - present...<br>
</font>
<form action="./pages/php/search_index.php">
<input id="link" type="submit" value="Search Current">
</form>
<br>
Search archive database
<br>
<font size="2pt">
(5,535,886 records)<br>
4 March 2014 - 30 October 2017<br>
</font>
<form action="./pages/php/search_full.php">
<input id="link" type="submit" value="Search Archive">
</form>
<br>
RX ID Search<br>
<form action="./pages/php/search_rx_dates.php">
<input id="link" type="submit" value="RX Search">
</form>
</td>
<td><center>
<font size="3">Coast Stations</font><br>
<form action="./pages/php/reu_all_index.html">
<input id="link" type="submit" value="Coast RWW">
</form>
<hr>
<font size="3">Ship Stations</font><br>
<form action="./pages/php/reu_ship_index.html">
<input id="link" type="submit" value="Ship RWW">
</form>

</td>
<!--<font size="3">All YaDDNet Members combined</font><br>
<form action="./pages/reu_all_index.html">
<input id="link" type="submit" value="All RX RWW Generator">
</form><br>-->
<!--
<font color=white><b>NEW!! </b></font><font size="3">Use only "NON-TEST" messages</font><br>
<form action="./pages/reu_nt_index.html">
<input id="link" type="submit" value="REU Generator">
</form><br>
-->



<td>

<center>
<form action="./pages/php/rx_active_list.php">
<input id="link" type="submit" value="Active RXs">
</form>
<br>

</td>
<td>
<center>
<form action="./pages/php/rx_online.php">
<input id="link" type="submit" value="Online RX (60 mins)">
</form>
<br>


<form action="./pages/php/rx_online_day.php">
<input id="link" type="submit" value="Online RX (24 hours)">
</form>
<br>

<form action="./pages/php/rx_online_month.php">
<input id="link" type="submit" value="Online RX (30 days)">
</form>
<br>

<form action="./pages/php/comp.php">
<input id="link" type="submit" value="RX Rate" />
</form>

</td>
</tr>
</table>

<hr width=80%>

<table cellpadding=5 rules=all>
<caption><b>Quick select of FMT / CAT / TC1</b></caption>
<th>Format</th>
<th>Category</th>
<th>Telecommand 1</th>
<th>Telecommand 1</th>
<tr>
<td>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=fmt type="submit" value="AREA" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=fmt type="submit" value="DIS" />
</form>
<!--<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=fmt type="submit" value="GRP" />
</form>
-->
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=fmt type="submit" value="ALL" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=fmt type="submit" value="SEL" />
</form>
</td>
<td>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=cat type="submit" value="RTN" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=cat type="submit" value="SAF" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=cat type="submit" value="URG" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=cat type="submit" value="DIS" />
</form>
</td>
<td>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="Test" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="J3E TP" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="F3E/G3E" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="UNABLE" />
</form>
</td>
<td>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="DISTRESS ACK" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="DISTRESS RELAY" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="POSUPD" />
</form>
<form action="./pages/php/quick_codes.php" method=GET>
<input id="link" name=tc1 type="submit" value="POLL" />
</form>
</td>
</tr>
</table>

<hr>
<!--<h3> <font color=white><b>NEW!! </b></font>Records from the new SQL Database started 8/8/17</h3>-->

<table border=0 cellpadding=5 rules='cols'>
<th>Messages from all RX<br>last 60 minutes</th>
<th>To or From any Coast stations<br> which use a Ship Station MMSI <br>Last 24 hours</th>
<th>UNID Coast Stations</th>
<th>Raw messages from YaDD</th>
<th>All columns from the new DB</th>


<tr>
<td>
<center>
<form action="./pages/php/live.php">
<input id="link" type="submit" value="All messages">
</form>
<br>
<!--
<form action="./pages/php/live_ok.php">
<input id="link" type="submit" value="OK messages">
</form>
</td>
-->
<td>
<center>
<form action="./pages/php/special.php">
<input id="link" type="submit" value="Specials">
</form>
</td>
<td>
<center>
<form action="./pages/php/unid_2.php">
<input id="link" type="submit" value="UNIDs">
</form>
</td>
<td>
<center>
<form action="./pages/php/raw.php">
<input id="link" type="submit" value="Messages">
</form>
</td>
<td>
<center>
<form action="./pages/php/fulldb.php">
<input id="link" type="submit" value="All Columns">
</form>

</td>
</tr>
</table>
<hr width=80%>


<h2><font color=#006666>Lists of Coast Stations received</font></h2>


<hr width=30%>
<center>
<b>Coast Stations logged per channel</b>



<form action="./pages/php/band_coast_today_stats.php" method="GET">

<br>
<table><caption><b>Time range</b></caption>
<tr>
<td>
<input type="radio" name="timescale" value="1" checked />1 day
</td>
<td>
<input type="radio" name="timescale" value="7" />7 days
</td>
</tr>
</table>


<table cellpadding=5>
<tr>
<td><center><input id="freq" type="submit" name="rx_freq" value="2177.0" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="2187.5" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="4207.5" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="6312.0" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="8414.5" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="12577.0"  /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="16804.5" /></td>
</tr>
</table>
<center>
<input id="freq" type="submit" name="rx_freq" value="All"  />
<br>All Channels
</form>
<br><br>
<hr width=30%>
<!--
<b>Coast Stations logged by Continent/MID (Today)</b>
<form action="./pages/php/mid_coast_today.php" method="GET">
<table cellpadding=5>
<tr>
<td><center><input id="freq" type="submit" name="mid" value="[200]" /><br>Europe/Russia</center></td>
<td><center><input id="freq" type="submit" name="mid" value="[300]" /><br>N.America/Caribbean</center></td>
<td><center><input id="freq" type="submit" name="mid" value="[400]" /><br>Asia/Middle East</center></td></tr>
<tr>
<td><center><input id="freq" type="submit" name="mid" value="[500]" /><br>Australasia/S.E. Asia</center></td>
<td><center><input id="freq" type="submit" name="mid" value="[600]" /><br>Africa</center></td>
<td><center><input id="freq" type="submit" name="mid" value="[700]" /><br>S. America</center></td>
</tr>
</table>
</form>
-->
<br>
<center>
<b>Coast Stations logged by Continent / MID</b>
<form action="./pages/php/coast_freq_today.php" method="GET">
<br>
<table><caption><b>Time range</b></caption>
<tr>
<td>
<input type="radio" name="timescale" value="1" checked />1 day
</td>
<td>
<input type="radio" name="timescale" value="7" />7 days
</td>
</tr>
</table>

<table cellpadding=5>
<tr>
<td><center><input id="freq" type="submit" name="mid1" value="[200]" /><br>Europe / Russia</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[300]" /><br>N.America / Caribbean</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[400]" /><br>Asia / Middle East</center></td></tr>
<tr>
<td><center><input id="freq" type="submit" name="mid1" value="[500]" /><br>Australasia / S.E. Asia</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[600]" /><br>Africa</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[700]" /><br>S. America</center></td>
</tr>
<tr>
<tr>
<td></td>
<td><center><input id="freq" type="submit" name="mid1" value="[ALL]" /><br>All MIDs</center></td>
<td></td>
</tr>
</table>
</form>

<hr width=80%>
<h2><font color=#006666>Lists of Ship Stations received</font></h2>
<h3> Previous 24 hours </h3>
<hr width=30%>

<center>
<b>Ship Stations logged per channel</b>
<br><br>
<form action="./pages/php/band_ship_today_stats.php" method="GET">


<br>
<table><caption><b>Time range</b></caption>
<tr>
<td>
<input type="radio" name="timescale" value="1" checked />1 day
</td>
<td>
<input type="radio" name="timescale" value="7" />7 days
</td>
</tr>
</table>


<input type="radio" name="order" value="MMSI" checked />Sort by MMSI
<input type="radio" name="order" value="Name" />Sort by Ship Name
<input type="radio" name="order" value="Country" />Sort by Country
<br>
<table cellpadding=5>
<tr>
<td><center><input id="freq" type="submit" name="rx_freq" value="2177.0" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="2187.5" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="4207.5" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="6312.0" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="8414.5" /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="12577.0"  /></td>
<td><center><input id="freq" type="submit" name="rx_freq" value="16804.5" /></td>
</tr>
</table>
<center>
<input id="freq" type="submit" name="rx_freq" value="All"  />
<br>All Channels
</form>
<br><br>
<hr width=30%>
<br>
<center>
<b>Ship Stations logged by Continent / MID</b>
<br><br>
<form action="./pages/php/ship_freq_today.php" method="GET">

<br>
<table><caption><b>Time range</b></caption>
<tr>
<td>
<input type="radio" name="timescale" value="1" checked />1 day
</td>
<td>
<input type="radio" name="timescale" value="7" />7 days
</td>
</tr>
</table>


<input type="radio" name="order" value="MMSI" checked />Sort by MMSI
<input type="radio" name="order" value="Name" />Sort by Ship Name
<input type="radio" name="order" value="Country" />Sort by Country
<br>
<table cellpadding=5>
<tr>
<td><center><input id="freq" type="submit" name="mid1" value="[200]" /><br>Europe / Russia</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[300]" /><br>N.America / Caribbean</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[400]" /><br>Asia / Middle East</center></td></tr>
<tr>
<td><center><input id="freq" type="submit" name="mid1" value="[500]" /><br>Australasia / S.E. Asia</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[600]" /><br>Africa</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[700]" /><br>S. America</center></td>
</tr>
<tr>
<tr>
<td></td>
<td><center><input id="freq" type="submit" name="mid1" value="[ALL]" /><br>All MIDs</center></td>
<td></td>
</tr>
</table>
</form>

<hr>

<!--
<h3> All Time </h3>
<font color=white><b>"All Time" searches will take several seconds, <br>due to the amount of data to sort, please be patient</font></b>
<hr width=30%>

<b>Coast Stations logged per channel (All Time)</b>
<form action="./pages/php/band_coast_all_time_stats.php" method="GET">
<table cellpadding=5>
<tr>
<td><input id="freq" type="submit" name="rx_freq" value="2177.0" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="2187.5" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="4207.5" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="6312.0" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="8414.5" /></td>
<td><input id="freq" type="submit" name="rx_freq" value="12577.0"  /></td>
<td><input id="freq" type="submit" name="rx_freq" value="16804.5" /></td>
</tr>
</table>


Coast Stations logged overall<br>
<td><input id="freq" type="submit" name="rx_freq" value="All"  /></td>
</form>





<hr width=30%>
<b>Coast Stations logged by Continent/MID, the frequencies logged, and the number of messages per frequency. (All Time) </b>
<form action="./pages/php/coast_freq.php" method="GET">
<table cellpadding=5>
<tr>
<td><center><input id="freq" type="submit" name="mid1" value="[200]" /><br>Europe/Russia</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[300]" /><br>N.America/Caribbean</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[400]" /><br>Asia/Middle East</center></td></tr>
<tr>
<td><center><input id="freq" type="submit" name="mid1" value="[500]" /><br>Australasia/S.E. Asia</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[600]" /><br>Africa</center></td>
<td><center><input id="freq" type="submit" name="mid1" value="[700]" /><br>S. America</center></td>
</tr>
<tr>
<td></td>
<td><center><input id="freq" type="submit" name="mid1" value="[ALL]" /><br>All MIDs</center></td>
<td></td>
</tr>
</table>
</form>

-->


<!--<table cellpadding=5 rules="cols">-->

<!--<th>Statistics for the SQL Database<br>Number of messages stored,<br> Number of Stations heard, etc.</th>-->
<!--<th>Statistics for the connected Receivers<br>Messages per RX<br>Coast Stations per RX, etc</th>-->
<!--<th>List of recent UNID Coaststations.</th>-->
<!--
<th>Full list of Coast Stations<br> and the frequencies they've been heard on</th>
<th>Statistics from the Apache Webserver<br>Visitors, Browsers used, etc.</th>
<tr>
<td><center>
<form action="./pages/php/db_stats.php">
<input id="link" type="submit" value="DB Stats">
</form></center>
</td>
-->
<!--
<tr>
<td><center>
<form action="./pages/php/rx_stats.php">
<input id="link" type="submit" value="RX Stats">
</form></center>
</td>

-->
<!--
<td><center>
<form action="./pages/php/unid.php">
<input id="link" type="submit" value="UNIDs">
</form></center>
</td>
-->

<!--
<td><center>
<form action="./webstat.html">
<input id="link" type="submit" value="Apache Stats">
</form></center>
</td>
-->
<!--</tr>
</table>
<hr width=80%>-->
<h2><font color=#006666>Additional Information</h2></font>

<!--<h3>Additional information</h3>-->
<table border=0 cellpadding=10 rules="all">
<th>Activity Log</th>
<th>Filtered Logs</th>
<th>MMSI database</th>
<!--<th>Extra Info</th>-->

<tr>
<td><form action="./pages/php/logger.php">
<input id="link" type="submit" value="All Logging">
</form>

</td>
<td>
<form action="./pages/php/logger_messages.php">
<center><input id="link" type="submit" value="All Input">
</form>
<!--<hr>
<form action="./pages/php/logger_udp.php">
<center><input id="link" type="submit" value="IP Addresses">
</form>
-->
<hr>
<form action="./pages/php/logger_resolver.php">
<center><input id="link" type="submit" value="Resolver">
</form>
<!--
YaDD Messages
<form action="./pages/php/logger_messages.php">
<center><input id="link" type="submit" name="svr_type" value="yUDP">
</form>
<br>
DSC Decoder Messages
<form action="./pages/php/logger_messages.php">
<center><input id="link" type="submit" name="svr_type" value="dUDP">
</form>
<br>
-->
<hr>
<form action="./pages/php/logger_purge.php">
<center><input id="link" type="submit" value="Database Management">
</form>
</td>

<td>
All ships, listed in<br>newest-first order<br>
<form action="./pages/php/mmsi_shipname.php">
<center><input id="link" type="submit" value="Ship Names">
</form>
<hr>
All ships, listed in<br>MMSI order<br>
<form action="./pages/php/mmsi_shipname_ordered.php">
<center><input id="link" type="submit" value="MMSI List">
</form>
<td><form action="./pages/php/test/">
<input style="background:#993333; color:white; width:140px; height:30px; border-radius:10px; cursor:pointer;" type="submit" value="Test Area">
</form>
<!--

<td>
<br>
<form action="./pages/php/test/logfile.txt">
<center><input id="link" type="submit" value="Logfile">
</form></td>
-->

</tr>
</table>
<!--<hr width=50%>
<form action="./logs">
<input id="link" type="submit" value="Masterlogs">
</form>
All messages collected by YmLOG, from all connected receivers. <br>
These can be used to retrieve the full messages, including DSC Symbols, and RAW FEC symbols.<br>
<font color=white size=4pt>Stored as ZIP files for faster download.</font><br>
-->
<hr width=50%>
<h4>Data is stored with the following criteria:</h4>
<b>Messages with Parity failures (~) or ECC checksum failures (ECC = ERR) are discarded at source and not stored.</b>
<!--
Messages with ECC checksum failures are purged after 24 hours<br><br>
Messages with ECC checksums correct, but with any of the following corruptions, are also purged after 24 hours:<br><br>
Symbol parity failures (~) in either MMSI <br>
Symbol parity failures (~) in Freq/Position data fields<br>
"UNK" values for Category (CAT), Telecommands (TC1/2) or EOS<br>
-->
<br>
<br>
<b> Ship Names are now automatically resolved via the <a href="http://aprs.fi/#!mt=roadmap&z=11&lat=60.2253&lng=-1.3508&timerange=86400&tail=86400" target="_BLANK"> APRS.FI </a>web API</b><br>
<br>
If this is unsuccessful the ITU MARS database is used, followed if necessary by the Marine Traffic website.
<br><br>
<hr width=80%>


<b>YaDDNet also provides RX facilities for Snargate Radio, Dover (MMSI<i> 002320204</i>)</b><br>
<form action="./pages/php/test/tmp/snargate_status.html">
<center><input id="link" type="submit" value="Snargate Status">
</form>

<hr width=80%>
<b>For more DSC Monitoring information, join the DSC-List at <a href="https://groups.yahoo.com/neo/groups/dsc-list/info"  >https://groups.yahoo.com/neo/groups/dsc-list/info</a></b><br>
<br>
My <a href="./pages/MF_and_HF_DSCguide.pdf"  >Guide to MF/HF DSC</a><br>
<br>
The DSC Bible from the ITU : <a href="./pages/DSC.pdf"  >R-REC-M.493</a><br>
<br>

<hr width=50%>
<font size=4pt>Powered by <b>YaDD</b> <i>"Yet another DSC Decoder"</i>
<br>
with a lot of help from <b>Python, PHP and MySQL</b></font>
<br><br>
Website written entirely by hand using <a href="http://www.vim.org/">ViM</a>
<br>
<br>
gm4slv at gmail dot com

</center>
</body>
</html>

