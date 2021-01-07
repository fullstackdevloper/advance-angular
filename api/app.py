from flask import Flask, render_template, jsonify
from flasgger import Swagger
import requests
import lxml.html
from flask_api_cache import ApiCache

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET"),
        ('Access-Control-Allow-Credentials', "true"),

    ],
    "specs": [
        {
            "version": "0.0.1",
            "title": "Category Api",
            "endpoint": '/api/v1',
            "route": '/api/v1',

        }
    ]
}

Swagger(app)


@app.route('/api/v1/categories/<param>/')
def getCatagories(param):
    """Example endpoint returning a list of categories by param
    This is using docstrings for specifications.
    ---
    parameters:
      - name: param
        in: path
        type: string

        required: true
        default: all
    definitions:
      Param:
        type: object
        properties:
          param_name:
            type: string
            items:
              $ref: '#/definitions/Category'
      Category:
        type: string
    responses:
      200:
        description: A list of Category (may be filtered by Param)
        schema:
          $ref: '#/definitions/Param'

    """
    html = requests.get("https://www.theepochtimes.com/")
    doc = lxml.html.fromstring(html.content)
    categories = doc.xpath(
        '//ul[@id="menu-front-page-primary"]/li/a/text() | .//ul[@id="menu-front-page-primary"]/li/a/@href')
    new_strings = []
    for string in categories:
        new_string = string.replace("https://www.theepochtimes.com/", "")
        new_strings.append(new_string)

        init = iter(new_strings)
    res_dct = dict(zip(init, init))
    return res_dct


@app.route('/api/v1/categorybyslug/<slug>/')
def getCatagoryBySlug(slug):
    """Example endpoint returning a list of category content by slug
    This is using docstrings for specifications.
    ---
    parameters:
      - name: slug
        in: path
        type: string
        enum: ['c-business', 'c-arts-culture', 'c-china']
        required: true
        default: c-arts-culture
    definitions:
      Slug:
        type: object
        properties:
          slug_name:
            type: string
            items:
              $ref: '#/definitions/CatagoryBySlug'
      CatagoryBySlug:
        type: string
    responses:
      200:
        description: A list of Category Content (may be filtered by slug)
        schema:
          $ref: '#/definitions/Slug'

    """
    html = requests.get('https://www.theepochtimes.com/'+slug)
    doc = lxml.html.fromstring(html.content)
    new_releases = doc.xpath('//div[@class="main_content"]')[0]
    gettiles = new_releases.xpath('//div[@class="left_col"]')[0]
    titles = gettiles.xpath('//div[@class="title"]/a/text()')
    desr = gettiles.xpath('//div[@class="excerpt more_info"]/text()')
    ptime = gettiles.xpath('//span[@class="time"]/text()')
    imgs = gettiles.xpath('//div[@class="image"]/a/img/@data-src')

    output = []
    for info in zip(titles, desr, ptime, imgs):
        resp = {}
        resp['title'] = info[0]
        resp['description'] = info[1].strip()
        resp['time'] = info[2]
        resp['image'] = info[3]
        output.append(resp)
    return jsonify(output)


@app.route('/api/v1/topnews/')
@ApiCache(expired_time=86400)
def Topnews():
    """Example endpoint returning a list of top news
      This is using docstrings for specifications.
      ---
      parameters:
        - name: slug
          in: path
          type: string
          required: false
          default: recent
      definitions:
        Slug:
          type: object
          properties:
            slug_name:
              type: string
              items:
                $ref: '#/definitions/Topnews'
        Topnews:
          type: string
      responses:
        200:
          description: A list of top news
          schema:
            $ref: '#/definitions/'

      """
    html = requests.get('https://www.theepochtimes.com/')
    doc = lxml.html.fromstring(html.content)
    new_releases = doc.xpath('//ul[@id="frontpage_topnews_list"]')[0]
    titles = new_releases.xpath('//div[@class="left_part"]/a/span/text()')
    images = new_releases.xpath(
        '//ul[@id="frontpage_topnews_list"]/li/a/span/img/@data-src')
    output = []
    for info in zip(titles, images):
        resp = {}
        resp['title'] = info[0]
        resp['image'] = info[1]
        output.append(resp)
    return jsonify(output)


if __name__ == '__main__':
    app.run()
