---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "When Less Is More?"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2020-01-23T09:33:56-04:00
lastmod: 2020-01-23T09:33:56-04:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

For my graduate project I am trying to grow a community of microbes together. The main problem I’m facing is that putting many species together is not a guarantee they will survive, some will go “extinct” in my experiment.To do that, two different postdoctoral students advised me to use a minimal and defined media, like M9 with glucose, since this forces the different species to interact. But eliminating resources to increase diversity seemed counterintuitive to me. For instance, what is more diverse? The resource- and water- rich Amazon forest, or the desert?

On the other hand, growing communities in a minimal media seemed to be the norm. It was used in both [“Emergent simplicity in microbial community assembly”](https://science.sciencemag.org/content/361/6401/469) and [“Clustering in community structure across replicate ecosystems following a long-term bacterial evolution experiment,”](https://www.nature.com/articles/ncomms5643) two papers that really inspired my project.

I came up with 3 possible explanations why minimal media are actually used to grow microbial communities:

1) A minimal media does lead to more community diversity, by forcing microbes to interact rather than compete
2) A minimal medium slows down fast-growing bacteria enough to see slow-growing bacteria
3) Well-defined mediums are a good “control” for microbial ecology, and defined mediums tend to be minimal media

I found some support for point (1) in ["Costless metabolic secretions as drivers of interspecies interactions in microbial ecosystems"](https://www.nature.com/articles/s41467-018-07946-9). In this paper, the authors constructed a computer simulation to give one answer to how come we find so much diversity in resource-poor environments? They simulated many species pairs on many 2-carbon mediums. If one specie could grow on the medium, they added its metabolites to the medium and fed it back to the two organisms recursively until now new metabolites were added to the medium.

I would think that this essentially creates a “rich gets richer” principle. Any excretion essentially creates a new metabolite a new species can feast on. That species in return excretes a different metabolite, which then opens the niche for another specie to consume it and excrete another metabolites. More microbes enrich the environment, which in turn invite more microbes.

his paper makes two important points. One, that a minimal media does force interaction between species (in the form of relying on one another’s metabolites) and two, that it does allow a more diverse community than initially predicted. However, it doesn’t prove that a poor media would create a more diverse community than a rich media.

But then, there might be a different reason why I specifically should use a minimal media. The reason is that I don’t want to grow my community, I also want to evolve it. At least according to [“Structure and Evolution of Streptomyces Interaction Networks in Soil and In Silico”](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001184) more interactions increases the rate of evolution in an organism, and on any hand more interaction-related mutations will make a more interesting direction of evolution (the alternative is tracking the organisms’ evolution to fit to this specific medium, which is not so interesting).

There is also a way to experimentally test which media is best for communities. I can grow my communities on an M9 media with one measure of glucose versus 5 times the glucose, and I can grow them on LB media at the normal amount versus 1/5 of the amount. But then I also start getting into trouble.

For instance, am I not just comparing M9 to LB? Maybe I should use a larger diversity of media? Also, which community should I use? From the sea, the soil, sewage, or my stomach? What about extremophiles?

It’s very hard to make such a universal statement in microbial evolution. A more realistic solution will probably be a simulation.
