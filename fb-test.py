import webapp2
from urllib2 import urlopen
from json import load
import gviz_api

html1="""
<!doctype html>
<html>
    <head>
        <title> Facebook Ultimate Data Fetching App</title>
    </head>
    <body>
        <h2>Facebook Ultimate Data Fetching App</h2>
        <style>
            h2 {
            font: bold 330%/100% "Lucida Grande";
            position: relative;
            color: #464646;
}
             
        </style>
        <form method="post">
            <lable for="query1">Company1:</lable>
            <input name="query1", type="text", value='gap'><br>          
            <lable for="query2">Company2:</lable>
            <input name="query2", type="text", value='bananarepublic'><br>
            <lable for="query3">Company3:</lable>
            <input name="query3", type="text", value='jcrew'><br>          
            <lable for="query4">Company4:</lable>
            <input name="query4", type="text", value='coach'><br>
            <lable for="query5">Company5:</lable>
            <input name="query5", type="text", value='burberry'><br>
            <p><b>Please input interested companies to perform competitive analysis, up to 5 companies</b></p>
            <input type="submit", value="submit query"><br>
               
        </form>
    </body>
</html>



"""

page_template = """
<html>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>

  <!--draw table-->
    google.load('visualization', '1', {packages:['table']});

    google.setOnLoadCallback(drawTable);
    function drawTable() {
      %(jscode)s
      var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
      jscode_table.draw(jscode_data, {showRowNumber: true});
      
    }

    <!--draw two charts-->
    google.load("visualization", "1", {packages:["corechart"]});
    
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        %(jscode1)s
        %(jscode2)s
      
        var options1 = {
          title: 'How many fans it has',
          hAxis: {title: 'company', titleTextStyle: {color: 'red'}}
        };
        var options2 = {
          title: 'How many times people are talking about this',
          hAxis: {title: 'company', titleTextStyle: {color: 'red'}}
        };

        var jscode_chart1 = new google.visualization.ColumnChart(document.getElementById('chart1_div_jscode'));
        jscode_chart1.draw(jscode_data1, options1);

        var jscode_chart2 = new google.visualization.ColumnChart(document.getElementById('chart2_div_jscode'));
        jscode_chart2.draw(jscode_data2, options2);
        
      }

  </script>
  <body>
  <style>
  div{
     display:block
     }
  </style>
    <H1>How Hot Each of Them is on Facebook?</H1>
    <div id="table_div_jscode"></div>
    <div id="chart1_div_jscode"></div>
    <div id="chart2_div_jscode"></div>
    
  </body>
</html>
"""


class MainPage(webapp2.RequestHandler):
        
    def get(self):
        self.response.write(html1)

    def post(self):
        query_list=[]
        for i in range (1,6):
            query_list.append(self.request.get('query'+str(i)).encode('ascii','ignore'))
        if not query_list:
            self.response.write('blanket inquery!')
        datastore={}
        datastore1={}
        datastore2={}
        base_url = 'https://graph.facebook.com/'
        
        for query in query_list:
            try:
                url=base_url+query+'access_token=****'
                response=urlopen(url)
                js=load(response)
                name=js['name']
                likes=js['likes']
                TAC=js['talking_about_count']
    
                datastore[query]={'name':name,'likes':likes,'TAC':TAC}
                datastore1[query]={'name':name,'likes':likes}
                datastore2[query]={'name':name,'TAC':TAC}
            except Exception,e:
                continue
 
        description1={'name':('string','Company name'),
                      'likes':('number','Likes')}
        description2={'name':('string','Company name'), 'TAC':('number','people talking about this')}
        description={'name':('string','Company name'),
                     'likes':('number','Likes'),
                     'TAC':('number','people talking about this')}
        data1=datastore1.values()
        
        data2=datastore2.values()
        
        data=datastore.values()   
        # Loading it into gviz_api.DataTable
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        data_chart1 = gviz_api.DataTable(description1)
        data_chart1.LoadData(data1)
        data_chart2 = gviz_api.DataTable(description2)
        data_chart2.LoadData(data2)
        # Creating a JavaScript code string
        jscode = data_table.ToJSCode("jscode_data",
                                     columns_order=("name", "likes", "TAC"),
                                     order_by="likes")
        jscode1 = data_chart1.ToJSCode("jscode_data1",
                                     columns_order=("name", "likes"),
                                     )
        jscode2 = data_chart2.ToJSCode("jscode_data2",
                                     columns_order=("name", "TAC"),
                                     )
        # Putting the JS code and JSon string into the template
        self.response.write(page_template % vars())
            
    
            
        
        
            
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)






















        
