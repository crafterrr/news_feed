<a href="/update_news">To the main page</a>
<table border=1>
    <tr>
        <th>Title</th>
        <th>Author</th>
        <th>#likes</th>
        <th>#comments</th>
    </tr>
    %for row in rows:
        <tr bgcolor={{row[1]}}>
            <td><a href="{{row[0].url}}">{{row[0].title}}</a></td>
            <td>{{row[0].author}}</td>
            <td>{{row[0].points}}</td>
            <td>{{row[0].comments}}</td>
        </tr>
    %end
</table>