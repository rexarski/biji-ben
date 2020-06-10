## Background

Data mining does boost the skyrocketing of technologies companies built upon recommendation algorithms. It provides multi-dimensional  information towards each individual service user, so that the company is able to understand its audience and more personalized intending service is able to be arranged. Nevertheless, some ethical issues are discovered at the same time. In this short essay, we are going to discuss the case of Netflix, its potential ethical concerns and suggestive fixes. 

## the project

### aims

As one of the most competitive streaming services in the market, Netflix could never achieve its accomplishment today without help of its recommendation system. The ultimate goal of such system is to provide personalized streaming experience to different kinds of customers, by presenting attractive options for them to choose from.

### methods

So the core of this algorithm, is how to find movies or TV plays this specific customer would like to watch. As Netflix’s vice president of product innovation, Todd Yellin, mentioned a very interest metaphor in an interview by WIRED[^1] last year, "The three legs of this stool would be Netflix members; taggers who understand everything about the content; and our machine learning algorithms that take all of the data and put things together".  Everyday, millions of Netflix users generate a huge amount of data such as what people watch, "What we see from those profiles is the following kinds of data – what people watch, what they watch after, what they watch before, what they watched a year ago, what they’ve watched recently and what time of day". After that, to understand the raw data better, Netflix has freelancers and in-house staff to tag the content by various standards. And finally, a machine learning algorithm is applied to figure out the behaviour of customers and put some weights over the previous two "legs" and form so-called "taste communities" such that people would be recommended the same kind of things popular among people like them. To conclude the general idea of this algorithm, it is a clustering algorithm done by a mixture of unsupervised and supervised learning. The clustering itself is unsupervised, however, the taggers indeed provide some extra information as guidance towards the content watched.

### source and nature of data

Obviously, a majority of the data comes from what people have watched, whether they finished watching it etc. But this is not the whole story, the data involved in this mining procedure not only comes from a direct feedback, such as a 'thumb-up' after watching or adding to My List, but some implicit behaviour data as well. These kinds of data are more 'behaviour' related, or more humanly. It is about how you watched a TV series rather than just a binary feedback. For example, if you watch it continuously for two nights, instead of few episodes every week, you probably are really into the plot of this series. Moreover, Netflix also collects information about users' playing devices, internet provider and geo-location, etc.

### the authority of data access 

According to Netflix's Privacy Statement [^2], the personal information is used for the betterment of user experiences, but Netflix has not ruled out the possibility of disclosing data to third parties. Generally speaking, the data might be disclosed if it satisfies legal process or government request. Moreover, the information will be transfered, if Netflix is involved in any reorganization, restructuring, merger or sale, or other transfer of assets.

### expected and unexpected results

The outcome of this evolving recommendation system cannot be simply unseen since Netflix is in fact doing better and better in its streaming media area. Additionally, the recommendation system is refined with one new aspect, which is personalized visuals based on each member's preference[^3].

![img](stranger-things.png)[^4]

With the support of a great deal of user-provided preferences, Netflix expanded its specilization into film and television production in 2013. This move is somewhat as expected, because as a company understanding the viewers so much, it is a hardly a risky move to make profits on it.

The only thing that overshadows this successful product is the privcy concerns it provokes. In December 2017, a tweet[^5] on Netflix's account stating that 53 people have watched A Christmas Prince every day for the past 18 days was considered 'creepy'. This tweet also raised a disccusion about the privacy of online streaming services. The current of these commercial companies like Netflix and Spotify, are starting to use anonymous user data in their marketing campaign[^6]. But what if the data gathered by Netflix's recommendation system is compromised? What if the algorithm understands too much and backfires? These questions are not currently on the surface, but still unavoidable.

## Ethical Issues

One thing that cannot be denied is that ethical issues are lurking inside the commercial success. In the following paragraphs, we are going to discuss some potential possibilities.

### Biased decisions

"[Algorithms] replace human processes, but they’re not held to the same standards,” Cathy O’Neil, the author of _Weapons of Math Destruction_, says, “People trust them too much.”

In the context of recommendation system, we know that basically everything we see within the range of Netflix service, is a result of recommendation. Surely we can trust the algorithm full-heartedly, but it is quite obvious that algorithm bias is gradually becoming a social issue along with the development of machine learning. For instance, a customer of a certain ethnicity might be recommended a lot of movies starred by actors or actresses of the same ethnicity, this could have negative consequences for minorities.

Let us take a look at the Principles for Algorithmic Transparency and Accountability issued by Associatin for Computing Machinery, and try to figure out if biased recommendation results violate these principle.

The first principle states that 'owners, designers, builders, users, and other stakeholders of analytic systems should be aware of the possible biases involved in their design, implementation, and use and the potential harm that biases can cause to individuals and society'. That is to say, companies should be aware of the the fallout of discrimination inside their recommendation algorithm. Meanwhile, the seventh principle emphasizes the role of validation and testing. It claims that algorithms should be tested for discriminatory harm, and make the results public. 

However, the status quo of recommendation algorithm is not optimistic, even though no cases about Netflix have appeared, similar issues did happen to large companies like Google, which once confused photos of gorillas and African american people[^7]. And this 'bug' still haunted them due to the shorthand of current machine learning algorithm. Hence, censoring certain search entries has been the most commonly used solution. Hopefully, the biased view of algorithm can be resolved more intelligently in the future.

### Individual privacy

Another obvious ethical aspect is the privacy of individual information. It not only includes personal information like name, address, payment methods, which are basic components of user information as any other online paid services, but also all behaviour-related information that illustrates an individual. As mentioned in the project description part, Netflix also records how people watch online streaming contents, for a better understanding of its customers.

This seems to agree with the fifth (data provenance) and sixth (auditability) principles of the 7 Principles. In this way, keeping data is useful and necessary. Now here comes an important question, what if these numbers are revealed to the public?

Interestingly, some aggregated statistics of users' behaviours reflect the status of popular culture, and people love to see them as fun facts, even a method to keep themselves on trend.The trending videos on YouTube and year-end summary done by Netflix and Spotify are such examples. But what if these statistics are narrowed down to some specific group of people, even to some anonymous individuals? Sometime, people could feel being targeted or even stalked in this case, that might be the origin of 'creepiness' in the Netflix's tweet debate. It is hard to say that people can stay totally anonymous on Internet today, and personal data leak is always a potential risk. But if we consider such summary statistics as a 'aggregated leak', for what level people can stand it? Therefore, it is should be carefully considered when a commercial company wants to reveal some fun facts about its customers, otherwise, people might not be entertained as expected. 

### Quality of Life

Streaming services like Netflix do improve the quality of life of their users, but the that does not mean to make all the choices with an excuse like 'for their own good'. Among all the data Netflix collects from its users, the internet provider detail is included. In 2017, it was reported that some Internet providers like Verizon, AT&T and Telstra were throttling[^8] the download speed of Netflix when the data usage is close to monthly limit. Admittedly, this action seems reasonable, and it even can be considered as a benevolent move. Still, Netflix does deceive its customers to some extent since it never mentions controlling downloading speed subjectively. [^9] In its Terms of Service, it states as followed:

"The quality of the display of the streaming movies & TV shows may vary from computer to computer, and device to device, and may be affected by a variety of factors, such as your location, the bandwidth available through and/or speed of your Internet connection." 

That never mentions "by carrier", hence we believe such action is not suitable. Referring to Australian Computer Society's Code of Professional Conduct, Netflix appears to respect the enhancement of quality of life, but on the other hand, the code of honesty is violated. Admittedly, Netflix did not bring any cost to its customer, but saved internet fares for them potentially. However, honesty is an absolute standard and cannot be compromised. Netflix failed to make the mechanism of netspeed throttling public to its users, in a long run, it could cause problem of distrust.

## improvement on ethical issues

### on biased decisions

One possible way to prevent bias from happening is to remove those vairables that could cause bias such as ethnicity, or to find a way to compensate it. Tan, Caruana, Hooker and Lou implemented a transparent model distillation approach to audit black-box models so that the impacts of bias is hopefully eliminated.

The other solution is strengthen the human factor in decission making, for example, partially replace recommendation algorithm with human curator or combine these two parts together. Currently, the algorithm has not achieved a level that makes everyone satisfied, so we could use some help from ourselves.

### on individual privacy

For individual privacy, the ultimate way to protect privacy information like watching habits is to anounymouzie. This can be carried out by combining simiar data together and process with bulk encryption. Specifically, for some every similar data. Some other mining methods that preserve privacy include (...):

1. Randomization methods: Add noise to the data to conceal the raw data.
2. The k-anonymity and l-diversity methods: The k-anonymity makes a given record mapped to at least k other records in the data, and the l-diversity enforces intragroup diversity of sensitive values to ensure anonymization.
3. Distributed privacy preservation: Partition large dataset by subsets (horizontally) or by attributes (vertically).
4. Downgrading the effectiveness of data mining results: Can hide some data partially or slightly distort some classification rules.
5. Differential privacy: An algorithm which behaves nearly the same on two similar data.

Along with the development of technology, the de-anolymous algorithm is getting more and more powerful. In fact, the second Netflix Price was suspended due to an exposure of customer information to the competitors (…) Overall, technology easily outgrows the pace of legislation these days. This is rather not surprising since the legislation usually takes a comparatively long procedure but the burst of technology is in a flash. Therefore, besides technological preventions, we should also strengthen governmetnal guidance. Public education about privacy protection is also a significant complement. Only in the way of combining self-discipline of companies and governmental supervision, can the right of privacy be guaranteed to individuals. Some specific governanal and educational approach can be:

- Accelerate the legislation related to online private privacy.
- Set up supervise commision to ensure that the frontier technology applied to industry will follow the framework of current regulations, etc.

### on quality of life

Regarding the discussed ethical issue about quality of life, companies should be more responsible for the service they provide and be clear about the word usage in their documentations such as terms of service. One truth is pretty obvious that, if a company actually improves the quality of its users, it will win a good portion of marketshare. Otherwise, it will suffer from loss in a long run. Hence, we could say, a company should target the improvement of human lives for both the greater good and their own interest. Without doubt, no company would refuse profits from its point of view. There is nothing special we need to emphasize in this aspect.

## Conclusion

The power conferred on the recommendation algorithm by data mining, indeed changes the industry of online streaming, even the industry of entertainment. But it is a also a double-edged sword. The risk of privacy being invaded has never been this high in the past. It is a cliché, but saying 'greater power comes with greater responsibility' is never an empty talk. Companies like Netflix should be more responsible for data they collect, to its customers, and by ethical standards. After all, the goal of technological progress we make, is to ameliorate the world, and it should not be built on the cost of breaking any ethical standards.

## reference

[2007] How To Break Anonymity of the Netflix Prize Dataset <https://arxiv.org/abs/cs/0610105>

[2007] WHY 'ANONYMOUS' DATA SOMETIMES ISN'T <https://www.wired.com/2007/12/why-anonymous-data-sometimes-isnt/>

[2012] Netflix Recommendations: Beyond the 5 stars (Part 1)  <https://medium.com/netflix-techblog/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429>

[2012] Netflix Recommendations: Beyond the 5 stars (Part 2) <https://medium.com/netflix-techblog/netflix-recommendations-beyond-the-5-stars-part-2-d9b96aa399f5>

[2013] The Science Behind the Netflix Algorithms That Decide What You’ll Watch Next <https://www.wired.com/2013/08/qq_netflix-algorithm/>

[2014] 数据隐私和大数据 — 合规问题和注意事项 <https://www.isaca.org/Journal/archives/2014/Volume-3/Pages/Data-Privacy-and-Big-Data-Compliance-Issues-and-Considerations-Chi.aspx>

[2014] Big Data Lessons From Netflix <https://www.wired.com/insights/2014/03/big-data-lessons-netflix/>

[2014] Optimizing the Netflix Streaming Experience with Data Science <https://medium.com/netflix-techblog/optimizing-the-netflix-streaming-experience-with-data-science-725f04c3e834>

[2014] Kdd 2014 Tutorial - the recommender problem revisited <https://www.slideshare.net/xamat/kdd-2014-tutorial-the-recommender-problem-revisited>

[2015] Netflix’s Viewing Data <https://medium.com/netflix-techblog/netflixs-viewing-data-how-we-know-where-you-are-in-house-of-cards-608dd61077da>

[2015] The Netflix Recommender System: Algorithms, Business Value, and Innovation https://dl.acm.org/citation.cfm?id=2843948

[2016] Netflix lifted the lid on how the algorithm that recommends you titles to watch actually works <https://www.businessinsider.com.au/how-the-netflix-recommendation-algorithm-works-2016-2?r=US&IR=T>

[2017] Originals Born of Data Mining: Netflix’s Well-known Secret?  <https://medium.com/nimbly-aware/originals-born-of-data-mining-netflixs-well-known-secret-6f4f33c011c2>

[2017] This is how Netflix's top-secret recommendation system works <http://www.wired.co.uk/article/how-do-netflixs-algorithms-work-machine-learning-helps-to-predict-what-viewers-will-like>

[2017] How Netflix Uses Analytics To Select Movies, Create Content, and Make Multimillion Dollar Decisions <https://blog.kissmetrics.com/how-netflix-uses-analytics/>

[2016] Selecting the best artwork for videos through A/B testing https://medium.com/netflix-techblog/selecting-the-best-artwork-for-videos-through-a-b-testing-f6155c4595f6

[2017-12] Artwork Personalization at Netflix <https://medium.com/netflix-techblog/artwork-personalization-c589f074ad76>

[2017] Netflix and Spotify Ask: Can Data Mining Make for Cute Ads?  <https://www.nytimes.com/2017/12/17/business/media/netflix-spotify-marketing.html>

[2018] Gatekeeping Algorithms with Human Ethical Bias: The ethics of algorithms in archives, libraries and society <https://arxiv.org/abs/1801.01705>

[2018-01] THE SUBLIMINAL TRICK NETFLIX USES TO GET YOU TO WATCH ITS MOVIES & SHOWS <https://www.thrillist.com/entertainment/nation/how-new-netflix-recommendation-algorithm-works>

Netflix Terms of Use <https://help.netflix.com/en/legal/termsofuse>

Netflix Privacy Statement https://help.netflix.com/legal/privacy

Recommender Systems from an Industrial and Ethical Perspective <https://dl.acm.org/citation.cfm?id=2959101>

Wikipedia page, https://en.wikipedia.org/wiki/Netflix

2017 on Netflix - A Year in Bingeing https://media.netflix.com/en/press-releases/2017-on-netflix-a-year-in-bingeing

Beyond Netflix’s Hypocrisy: The Real ‘Throttling’ Debate https://techpolicycorner.org/beyond-netflix-s-hypocrisy-the-real-throttling-debate-900c46c6ba79

The Algorithms Aren’t Biased, We Are https://medium.com/mit-media-lab/the-algorithms-arent-biased-we-are-a691f5f6f6f2

When Algorithms Discriminate https://www.nytimes.com/2015/07/10/upshot/when-algorithms-discriminate.html

Biased Algorithms Are Everywhere, and No One Seems to Care https://www.technologyreview.com/s/608248/biased-algorithms-are-everywhere-and-no-one-seems-to-care/

Weapons of Math Destruction

WHEN IT COMES TO GORILLAS, GOOGLE PHOTOS REMAINS BLIND https://www.wired.com/story/when-it-comes-to-gorillas-google-photos-remains-blind/

Code-of-Professional-Conduct_v2.1

2017_usacm_statement_algorithms

Jiawei Han, Micheline Kamber, Jian Pei - 2011 - Data Mining Concepts and Techniques 3rd Edition

Verizon accused of throttling Netflix and YouTube, admits to “video optimization” https://arstechnica.com/information-technology/2017/07/verizon-wireless-apparently-throttles-streaming-video-to-10mbps/

Beyond Netflix’s Hypocrisy: The Real ‘Throttling’ Debate https://techpolicycorner.org/beyond-netflix-s-hypocrisy-the-real-throttling-debate-900c46c6ba79

New Research Aims to Solve the Problem of AI Bias in “Black Box” Algorithms https://www.technologyreview.com/s/609338/new-research-aims-to-solve-the-problem-of-ai-bias-in-black-box-algorithms/

Protecting Netflix Viewing Privacy at Scale https://medium.com/netflix-techblog/protecting-netflix-viewing-privacy-at-scale-39c675d88f45

Auditing Black-Box Models Using Transparent Model Distillation With Side Information https://arxiv.org/abs/1710.06169

Bias test to prevent algorithms discriminating unfairly https://www.newscientist.com/article/mg23431195-300-bias-test-to-prevent-algorithms-discriminating-unfairly/

Singel, R. (2010) Netflix Cancels Recommendation Contest After Privacy Lawsuit. WIRED. Available from: https://www.wired.com/2010/03/netflix-cancels-contest/ [Accessed: 13rd March 2018]



(Chandrashekar, Amat, Basilico & Jebara, 2017)

[^1]: http://www.wired.co.uk/article/how-do-netflixs-algorithms-work-machine-learning-helps-to-predict-what-viewers-will-like
[^2]: https://help.netflix.com/legal/privacy
[^3]: https://medium.com/netflix-techblog/artwork-personalization-c589f074ad76 
[^4]: Different Artwork for Stranger Things.
[^5]: https://www.telegraph.co.uk/technology/2017/12/12/creepy-netflix-tweet-viewers-tv-habits-provokes-privacy-concerns/ ()
[^6]: https://www.nytimes.com/2017/12/17/business/media/netflix-spotify-marketing.html
[^7]: https://www.wired.com/story/when-it-comes-to-gorillas-google-photos-remains-blind/ (Simonite, 2018)
[^8]: https://arstechnica.com/information-technology/2017/07/verizon-wireless-apparently-throttles-streaming-video-to-10mbps/
[^9]: https://techpolicycorner.org/beyond-netflix-s-hypocrisy-the-real-throttling-debate-900c46c6ba79

https://www.acs.org.au/content/dam/acs/rules-and-regulations/Code-of-Professional-Conduct_v2.1.pdf

https://www.acm.org/binaries/content/assets/public-policy/2017_usacm_statement_algorithms.pdf