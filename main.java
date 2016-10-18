package fr.ensibs.pastebin.crawler;

import java.io.IOException;
import java.util.concurrent.TimeUnit;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.concurrent.ThreadLocalRandom;

####################################################
# Exercice : Crawl pastebin and avoid being banned #
####################################################

/**
 *
 * @author gauthier
 */
public class main {

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     * @throws java.lang.InterruptedException
     */
    public static void main(String[] args) throws IOException, InterruptedException {
  
        //Initiate documents
        Document rawpage;
        Document post;
        
        //Proxy
        System.setProperty("http.proxyHost", "");
        System.setProperty("http.proxyPort", "");
        System.setProperty("http.proxyUser", "");
        System.setProperty("http.proxyPassword", "");

        //Get archive
        rawpage = (Document) Jsoup.connect("http://pastebin.com/archive").get();
        Elements payload = rawpage.select(".maintable > tbody > tr > td:nth-child(1) > a");
        
        for (Element tab : payload){
            
            //Crawl
            post = (Document) Jsoup.connect("http://pastebin.com"+ tab.attr("href")).userAgent(userAgentSwitcher.getRandomUserAgent()).get();
            Elements editor_name = post.select(".paste_box_icon > a");
            String title = post.getElementsByClass("paste_box_line1").attr("title");
            Elements content = post.select("#paste_code");
            
            //Show results
            System.out.println("############################################################################");
            System.out.println("# [ id   ]   " + tab.attr("href"));
            System.out.println("# [title ]   " + title);
            if (editor_name.isEmpty()){
                System.out.println("# [author]    unknown");
                System.out.println("############################################################################");
            }
            else {
                System.out.println("# [author]   " + editor_name.first().attr("href").substring(3));
                System.out.println("############################################################################");
            }
            
            System.out.println(content);
            
            //Temporize to avoid banning
            TimeUnit.SECONDS.sleep((int)(ThreadLocalRandom.current().nextInt(20, 35)));
        }   
    }
}
