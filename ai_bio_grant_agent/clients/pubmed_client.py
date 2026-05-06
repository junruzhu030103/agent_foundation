from typing import List, Dict
import requests
import xml.etree.ElementTree as ET
from config.settings import PUBMED_EMAIL, PUBMED_TOOL


class PubMedClient:
    ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def search_pmids(self, query: str, retmax: int = 20) -> List[str]:
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": retmax,
            "retmode": "json",
            "sort": "relevance",
            "tool": PUBMED_TOOL,
            "email": PUBMED_EMAIL,
        }
        res = requests.get(self.ESEARCH, params=params, timeout=60)
        res.raise_for_status()
        data = res.json()
        return data.get("esearchresult", {}).get("idlist", [])

    def fetch_details(self, pmids: List[str]) -> List[Dict]:
        if not pmids:
            return []
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "tool": PUBMED_TOOL,
            "email": PUBMED_EMAIL,
        }
        res = requests.get(self.EFETCH, params=params, timeout=90)
        res.raise_for_status()

        root = ET.fromstring(res.text)
        papers = []
        for article in root.findall('.//PubmedArticle'):
            pmid = article.findtext('.//PMID', default='')
            title = article.findtext('.//ArticleTitle', default='').strip()
            abstract_nodes = article.findall('.//Abstract/AbstractText')
            abstract = ' '.join([(n.text or '').strip() for n in abstract_nodes]).strip()
            journal = article.findtext('.//Journal/Title', default='').strip()
            year = article.findtext('.//PubDate/Year', default='').strip()

            authors = []
            for a in article.findall('.//Author'):
                ln = a.findtext('LastName', default='').strip()
                fn = a.findtext('ForeName', default='').strip()
                full = f"{ln} {fn}".strip()
                if full:
                    authors.append(full)

            papers.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": journal,
                "year": year,
                "authors": authors[:6],
            })
        return papers
