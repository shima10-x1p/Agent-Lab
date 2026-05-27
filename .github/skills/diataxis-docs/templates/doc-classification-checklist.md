# Diátaxis Classification Checklist

## Classification Questions

1. Does this document help the user act, or help the user understand/check information?
2. Is the user acquiring skill, or applying skill?
3. Is the document task-oriented, learning-oriented, information-oriented, or understanding-oriented?

## Classification

| If the document... | And the user is... | Then classify as... |
| ------------------ | ------------------ | ------------------- |
| informs action     | acquiring skill    | Tutorial            |
| informs action     | applying skill     | How-to guide        |
| informs cognition  | applying skill     | Reference           |
| informs cognition  | acquiring skill    | Explanation         |

## Smell Checks

Tutorial smell:

* It tries to teach by doing.
* It must be safe and guided.
* It should avoid unnecessary branches.

How-to smell:

* It solves a real task.
* It assumes the user already knows the basics.
* It focuses on action.

Reference smell:

* It lists facts, parameters, schemas, commands, constraints, or error codes.
* It avoids long explanations.
* It is structured like the product.

Explanation smell:

* It gives background, context, concepts, or reasoning.
* It helps the user understand the subject.
* It should not become a step-by-step guide.

## Split Rules

* If a Reference contains long background reasoning, move that part to Explanation.
* If a How-to contains full API details, link to Reference instead.
* If a Tutorial contains many real-world branches, move those branches to How-to.
* If an Explanation records one important design decision, move it to ADR.
* If a document mixes multiple user needs, split it.
