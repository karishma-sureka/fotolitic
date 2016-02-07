/**
 * Created by ksureka on 2/6/16.
 */
function getCredentials(cb) {
    var data = {
        'grant_type': 'client_credentials',
        'client_id': "ZmwoxYhjRxACXVDKbNkwm-W0y1DqIprTU3SKTYfr",
        'client_secret': "4vwW5uTw8jkKx47zTt3KrhfWHdVJEnYzjEMCQuXi"
    };

    return $.ajax({
            'url': 'https://api.clarifai.com/v1/token',
            'data': data,
            'type': 'POST'
        })
        .then(function(r) {
            localStorage.setItem('accessToken', r.access_token);
            localStorage.setItem('tokenTimestamp', Math.floor(Date.now() / 1000));
            cb();
        });
}

count = 1;
var urlList = {
    "images":["http://www.clarifai.com/img/metro-north.jpg",
        "https://www.petfinder.com/wp-content/uploads/2012/11/140272627-grooming-needs-senior-cat-632x475.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_March_2010-1.jpg",
        "http://c.fastcompany.net/multisite_files/fastcompany/poster/2014/01/3025003-poster-p-dog-2.jpg",
        "http://sites.psu.edu/siowfa15/wp-content/uploads/sites/29639/2015/10/cat.jpg"
    ]
};
//localStorage.clear();
localStorage.setItem("1","http://www.clarifai.com/img/metro-north.jpg" );
localStorage.setItem("2","https://www.petfinder.com/wp-content/uploads/2012/11/140272627-grooming-needs-senior-cat-632x475.jpg" );
localStorage.setItem("3","https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_March_2010-1.jpg" );
localStorage.setItem("4","http://c.fastcompany.net/multisite_files/fastcompany/poster/2014/01/3025003-poster-p-dog-2.jpg" );
localStorage.setItem("5","http://sites.psu.edu/siowfa15/wp-content/uploads/sites/29639/2015/10/cat.jpg" );

function postImage(imgurl) {
    console.log("Post Image" + imgurl.toString());
    var data = {
        'url': imgurl
    };
    //var accessToken = localStorage.getItem('accessToken');
    return $.ajax({
        'url': 'https://api.clarifai.com/v1/tag',
        'headers': {
            'Authorization': 'Bearer ' + 'NbiYl9IAsjm75XqjS8gef0rZEeZTnS'
        },
        'data': data,
        'type': 'POST'
    }).then(function(r){
        console.log(r);
        parseResponse(r, imgurl);
});
}

function parseResponse(resp, imgurl) {
    console.log("Parse Image" + imgurl.toString());
    var tags = [];
    if (resp.status_code === 'OK') {
        var results = resp.results;
        tags = results[0].result.tag.classes;
    } else {
        console.log('Sorry, something is wrong.');
    }
    //tags need to go into the data base against imgurl for aggregation
    var text = tags.toString().replace(/,/g, ', ');
    $('#tags').text(text);
    addToDb(tags, imgurl);
    return tags;
}

function runner(){

    run();
    analyzeDb();
}

function abc(obj){
    imgurl = obj.images[ij];
    postImage(imgurl);
}

function run() {
  var obj = JSON.parse(JSON.stringify(urlList));
  for (ij = 0; ij < obj.images.length; ij++) {
      setTimeout(abc(obj), 500);


    /*if (localStorage.getItem('tokenTimeStamp') - Math.floor(Date.now() / 1000) > 86400
        || localStorage.getItem('accessToken') === null) {
        getCredentials(function() {
            console.log(imgurl);
            postImage("Gen Cred()" + imgurl);
        });
    } else {
        console.log("Reg()" + imgurl);
        postImage(imgurl);
    }*/
    }
}

//PUT for all tags returned
//GET images for a particular tag - search
//GET (count) and get stats on tags - aggregation

function addToDb(tags, imgurl){
    var data = '{"tags":"{' + tags + '}"}';
    console.log(data + imgurl.toString());
    //localStorage.setItem(count.toString(), imgurl);
    return $.ajax({
        'url': 'http://localhost:9200/images123/image/' + count.toString(),
        'data': data,
        'type': 'PUT'
    }).then(function(r){
        count = count + 1;
        console.log(r);
    });
}

function analyzeDb(){
    var data = '{"query":{"query_string":{"query":"cat"}}}';
    return $.ajax({
        'url': 'http://localhost:9200/images123/image/_search',
        'data': data,
        'type': 'POST'
    }).then(function(r){
        console.log("Executed this!");
        console.log(r);
        parseSearch(r);
    });
}

function parseSearch(resp){
    obj = JSON.parse(JSON.stringify(resp));
    console.log("Comes till here!!!" + obj.hits.total);
    for(i = 0; i < obj.hits.total; i++) {
        console.log("Set Counts" + i.toString());
        tagList = obj.hits.hits[i]._source.tags;
        var res = tagList.split(",");
        for(ii = 0; ii < res.length; ii++) {
            if(ii == 0){
                res[ii] = res[ii].split("{")[1];
            }
            else if(ii == res.length-1){
                res[ii] = res[ii].split("}")[0];
            }
            console.log("Output:" + localStorage.getItem(res[ii]));
            if(localStorage.getItem(res[ii]) === NaN || localStorage.getItem(res[ii]) === null){
                counter = 1;
            }
            else{
                console.log("Inside:" + localStorage.getItem(res[ii]));
                counter = parseInt(localStorage.getItem(res[ii]));
                counter = counter + 1;
            }
            console.log(counter);
            localStorage.setItem(res[ii], counter.toString());
        }
    }
}