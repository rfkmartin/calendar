<?php

$db_host = '127.0.0.1'; // don't forget to change
$db_user = 'root';
$db_pwd = 'abc123';
$database = 'cal';

$part1=fopen("part1.txt","r");
echo fread($part1,filesize("part1.txt"));
fclose($part1);

$link = mysqli_connect($db_host, $db_user, $db_pwd);
if (!$link) {
    die("Can't connect to database");
}

if (!mysqli_select_db($link, $database)) {
    die("Can't select database");
}
$query = 'select menu_date,menu from menu where menu_date>=curdate() order by menu_date asc limit 5';
$result = mysqli_query($link, $query) or die('Query failed: ' . mysqli_error($link));
for ($i = 0; $i < mysqli_num_rows($result); $i++) {
    list($menu_date, $text) = mysqli_fetch_row($result);
    $menu['date'] = $menu_date;
    $menu['text'] = $text;
    $menu_list[$i] = $menu;
}

print('<div class="menu"><table border="1"><tr>');
for ($i=0;$i<5;$i++) {
    $dt=new DateTime($menu_list[$i]['date']);
    print('<th>'.$dt->format('D(M j)').'</th>');
}
print('</tr><tr>');
for ($i=0;$i<5;$i++) {
    print('<td valign="top">'.$menu_list[$i]['text'].'</td>');
}
print('</tr></table></div>');

$part2=fopen("part2.txt","r");
echo fread($part2,filesize("part2.txt"));
fclose($part2);
?>
