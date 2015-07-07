for i in {0..1}; do
  scrapy crawl dic -a idx=$i -o "$i.json" --logfile="log.log"
done
