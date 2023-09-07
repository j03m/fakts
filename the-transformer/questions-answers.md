# Transformers

The following is companion to:

It won't discuss the entire paper. However, it will contain points and explanation I collected
while reading the paper with GPT-4 as a companion.

### BLEU Score

BLEU (Bilingual Evaluation Understudy) is a metric for evaluating the quality of machine-generated translations. It measures how many phrases in the machine-generated translation are present in a reference translation, offering a way to quantitatively assess translation quality. BLEU scores range from 0 to 100, with higher scores indicating better translation quality. However, it's important to note that BLEU is not a perfect measure; it doesn't account for semantic meaning, and it's not effective for evaluating translations that are syntactically different but semantically equivalent.

#### Real-World Example:
In real-world applications, BLEU scores are often used as an initial filter to gauge the effectiveness of machine translation systems. For example, a company developing a translation service might use BLEU scores to compare different versions of their model or to benchmark against competitors. However, human evaluation is generally also used for a more nuanced understanding of translation quality.

#### Code Snippet:
You can compute BLEU score using Python's NLTK library like this:
```python
from nltk.translate.bleu_score import sentence_bleu
reference = [['this', 'is', 'a', 'test'], ['this', 'is' 'test']]
candidate = ['this', 'is', 'a', 'test']
score = sentence_bleu(reference, candidate)
```

### WMT 2014 English-to-French Translation Task

WMT (Workshop on Machine Translation) is an annual event where various tasks related to machine translation are proposed, and teams compete to build models that perform best on these tasks. The "WMT 2014 English-to-French translation task" refers to a specific task set during the 2014 WMT competition, aimed at translating text from English to French.

#### Real-World Example:
The WMT competitions are critical for academia and the industry, serving as a standardized benchmark for machine translation models. Companies and researchers often cite their models' performance on WMT tasks when publishing papers or releasing new translation services.

To sum up:
- **BLEU**: A numerical metric for evaluating machine translations.
- **WMT 2014 English-to-French Translation Task**: A specific machine translation challenge set during the 2014 WMT competition.

For further reading:
- BLEU: [BLEU: a Method for Automatic Evaluation of Machine Translation](https://www.aclweb.org/anthology/P02-1040.pdf)
- WMT: [WMT Competitions](http://www.statmt.org/wmt20/)


### Reducing Sequential Computation

The paragraph starts by mentioning the goal of "reducing sequential computation," which is critical for parallelization and thus quicker model training. In the context of machine learning, specifically in sequence-to-sequence models like those used for machine translation, sequential computation can be a bottleneck. Models like RNNs have to process each element in the sequence one after the other, making parallel computation challenging.

#### Real-World Example:
Imagine you're building a trading bot that processes time-series stock market data. If your model processes data in a sequential manner, it could be too slow to execute trades in real-time. Reducing sequential dependencies can lead to faster predictions and better real-time performance.

### ConvS2S, ByteNet, and Neural GPU

The paragraph mentions Extended Neural GPU, ByteNet, and ConvS2S as models that use convolutional neural networks (CNNs) to address this issue to some extent. These models try to compute hidden representations in parallel for all input and output positions, but they have limitations.

#### Real-World Example:
Let's say you're building a recommendation engine for a financial news website. You want to take into account not just individual user actions but the context in which those actions happen. Convolutional layers can capture this context to some extent, but the "distance" between the events might limit the model's effectiveness. 

### The Problem with Distant Positions

In ConvS2S and ByteNet, the cost of relating distant positions in the input or output sequences grows with the distance between those positions. This makes it difficult for the model to learn long-range dependencies.

#### Real-World Example:
Imagine you're analyzing financial time-series data where events today might be affected by events that occurred several days ago. Traditional CNNs and RNNs might find it challenging to capture these long-range dependencies effectively.

### The Transformer Model

The Transformer addresses these issues by using only attention mechanisms to compute representations, making it more efficient in learning long-range dependencies. The cost of relating two arbitrary positions is constant, making it computationally more efficient.

### Self-Attention

Self-attention allows the model to consider other parts of the input sequence when processing a particular element. This is useful for tasks where the context of individual elements can provide useful information.

#### Real-World Example:
In a stock prediction model, the price of a stock today might be influenced by not just the stock's own past prices but also by the prices of related stocks. Self-attention allows the model to consider all these factors simultaneously.

#### Code Snippet for Self-Attention:
Here's a simplified Python code snippet to give you an idea of how self-attention might be implemented:
```python
import numpy as np

def self_attention(Q, K, V):
    # Calculate attention scores
    scores = np.dot(Q, K.T) 
    # Softmax
    attention_scores = np.exp(scores) / np.sum(np.exp(scores), axis=1, keepdims=True)
    # Calculate new values
    new_values = np.dot(attention_scores, V)
    return new_values
```

### End-to-End Memory Networks

These use recurrent attention mechanisms and are good for specific tasks like question answering and language modeling, but they still rely on sequence-aligned recurrence, unlike the Transformer.

### Summary

The Transformer model is unique in that it solely relies on self-attention mechanisms to process sequences, making it efficient both computationally and in terms of learning capabilities.

### Self-Attention in Context

Self-attention works by allowing each element in a sequence to focus on all other elements, weighted by their relevance. The "relevance" is determined through learned parameters. This is unlike RNNs, which maintain a hidden state and update it sequentially, thus potentially losing information from earlier parts of the sequence.

In self-attention, you have three main components for each element in the sequence:
- Query (Q)
- Key (K)
- Value (V)

The Query is used to find out what to focus on. The Key helps determine the relevance of other elements in relation to the Query. Finally, the Value is the actual content that we want to summarize or focus on.

### Understanding Self-Attention with a Real-World Example

Suppose you're analyzing time-series data from the stock market. Each data point could be a vector that includes various metrics like price, volume, etc., at a specific time.

1. **Query**: This could represent the current time point you're interested in.
2. **Key**: These would represent all time points, helping you figure out how relevant each other time point is to your current focus (the Query).
3. **Value**: These are also all time points, but now weighted according to the relevance computed between Query and Key. This provides a context-aware representation of each time point.

The computed "new values" after self-attention would then be a weighted summary of all other time points, focused around the time point of interest. This is particularly useful if events in the distant past might have an impact on the present, as the self-attention mechanism can capture these long-range dependencies efficiently.

In financial time-series data, for instance, self-attention could help a model consider the influence of a significant price drop two weeks ago when predicting the price for today.

### How It Relates to Transformers

In Transformers, this self-attention mechanism is used to replace sequence-dependent computations entirely, which makes it much faster and capable of parallelization. It also allows the model to focus on different parts of the input sequence when computing the representation for a specific element, making it more context-aware and efficient at capturing long-range dependencies.

### Intuition Behind Weighted Summary

Imagine you're in a noisy room full of people talking about various topics—sports, politics, movies, etc. You're trying to focus on a particular conversation about finance, a topic you're interested in. Your brain essentially performs a form of "attention" by tuning into the finance conversation and filtering out the other discussions. Your "awareness" at that moment is a weighted summary of all conversations in the room, heavily focused on the finance talk.

Similarly, in self-attention, each data point (or "time point" in the context of time-series data) gets to "focus" on all other points in the dataset, but not equally. It assigns different weights to different points based on their relevance or importance to the point in question.

### Focused Around a Time Point of Interest

Now let's say you're working on a stock market prediction model, and you're interested in predicting the stock price at a specific time \( t \).

- The "Query" represents the metrics at time \( t \) that you're interested in.
- The "Keys" are like the tags or descriptors for all other time points, helping you to identify which ones are relevant for the current prediction.
- The "Values" are the actual metrics at all time points.

Through self-attention, the model calculates a weighted average of all other time points, based on how relevant they are to time \( t \). This weighted average serves as a new, context-rich representation of time \( t \), which the model can then use for more accurate predictions.

### Real-World Example in Finance

For instance, if you're trying to predict a stock's future price, the self-attention mechanism could help the model focus on time points when similar price patterns occurred, or when significant financial events like quarterly reports were released. This way, the prediction at time \( t \) is not just based on the metrics at \( t \) but is a weighted summary of all relevant information across time.

### Summary

The idea is to create a new representation of each time point that is a weighted summary of all other time points, focused around its own specific metrics and features. This enables the model to capture complex relationships and dependencies, both near and far, in the data.

### What are the Keys?

In the self-attention mechanism, the Query, Key, and Value are often derived from the same initial set of vectors that represent the input sequence. These initial vectors might contain information about each time point in a time-series dataset, each word in a sentence, or each item in a list, depending on the application. These vectors are transformed into Query, Key, and Value vectors using separate learned weight matrices.

### How Are Keys Used?

The Keys are used to assess the relevance or similarity between the Query and all other points in the sequence. Specifically, the dot product is taken between the Query and each Key, and this produces a set of scores. These scores are then passed through a softmax function to produce attention weights, which sum up to 1. These attention weights are used to take a weighted sum of the Values, which gives the output for the particular Query.

### Real-World Example

Let's continue with the stock market example. Suppose you're analyzing stock price data at different time points. Each time point is represented by a vector containing features like price, volume, and other technical indicators.

- **Query for time \( t \)**: Represents the features at time \( t \) you're trying to analyze.
- **Keys for all times**: Each time point has its own Key, derived from its feature vector. These Keys serve as descriptors that help the model understand how relevant each time point is to time \( t \).
  
When calculating the attention for time \( t \), the Query for \( t \) is compared to the Keys for all time points (including \( t \) itself). The similarity scores tell the model how much focus or "attention" it should give to each time point when considering time \( t \).

### Intuition

Think of the Key for each time point as a sort of "label" or "descriptor" that captures its essence. When you're interested in a specific time point (the Query), you compare its "label" to the "labels" of all other time points (the Keys). The more similar the labels, the more attention the Query pays to those specific time points when creating its new, context-rich representation.

### Summary

In summary, the Keys are derived from the same initial input vectors as the Query and Values, and they serve to assess the relevance of each point in the sequence when calculating the attention mechanism. The model learns the optimal way to compute these Keys during the training process via gradient descent.

I hope this clarifies how Keys work and how they're used to compute weighted relevance in self-attention. Would you like to go into more detail on any of this?