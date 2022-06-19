# Cloud Resume Challenge
06/21/2022

## Introduction

Coming from a Software Dev background, I have always been interested in the mysterious Cloud, and wanted to learn more of the inner workings, but had no idea where to start. It was not until a good friend of mine, [Dakota Riley](https://www.linkedin.com/in/dakota-riley-b48401b7/), gifted me [Forrest Brazeal's Cloud Resume Challenge](https://cloudresumechallenge.dev/) book, where I finally took the dive, put my head down, and immersed myself.

## Preparation
I read Forrest Brazeal’s book. It points you in the right directions on how to tackle each step, while also providing inspiring stories on how the challenge has helped people make career changes. If you haven’t read it, I would recommend it.  

I first read through some of the AWS White Paper, and went through the [CCP digital course](https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/).

I then purchased [Adrian Cantrill’s SAA course](https://learn.cantrill.io/p/aws-certified-solutions-architect-associate-saa-c02).
This course is very thorough, and I cannot recommend it enough. I went through the AWS Fundamentals section to get a better grasp of the AWS concepts, and how they tie together. Plus, it doubles as training to take the SAA certification – the gold standard certification for the Cloud Industry, and a personal goal of mine to achieve.

## My Journey

### Static Website, CloudFront, and ACM:

![front-end](https://i.imgur.com/gJc4bqF.gif)

I started with just a basic HTML web-page, reminisce of the Angelfire/Geocities days, but just adding html format tags to my existing resume document. I just wanted to ensure that I had a working model, and that it would display with S3. 

I then purchased a domain-name using Route 53, and it was only $12 – Score!

After purchasing the domain, I immediately went into S3, and created a bucket that mirrored the domain-name. Upon creation, I uploaded my files from my local machine, and then edited the properties to enable Static website hosting. However, This gave me a bucket website end-point, which didn’t quite match my domain I just purchased.. but at least I had a working model!  This is where CloudFront came into play. 

Navigating to the CloudFront console, I found it excited that the Origin Domain was populated within the drop-menu. Awesome, that makes it easy! Before creating the distribution, I needed to request an SSL certificate, which is done through ACM (Amazon Certificate Manager).

I found ACM super neat – it took all the trouble of generating certificates, and automated most of it for you by creating the necessary CNAME records automagically.  Now that this was done, my CloudFront can be created, and tied to this certificate. However, this still didn’t fix everything, as my domain didn’t quite populate the static website yet.  I had to move back to Route53, and create a simple route that pointed my domain, to my CloudFront domain name.  After doing so, a few minutes later my domain populated my static website properly. Now we’re getting a move on things.

### DYNAMODB AND LAMBDA:

![lambda](https://user-images.githubusercontent.com/7934145/174809824-b4a45a64-f8a7-406e-8c88-f20cb2fc9d74.png)

Now, we needed to add a Visitor Count to our website, in which that data is stored in a DynamoDB. I was most excited about this part of the challenge, as writing serverless functions and NoSQL databases were something I’ve always wanted to dip my toes into. I have quite a bit of experience with tSQL, but NoSQL was a whole different beast. I started by going to the DynamoDB console, and just creating a table with the visitor partition key. I then gave this an item of VisitorCount, with a value of visitor_counter (Number). With that out of the way, we’re onto Lambda.

Lambda seemed intimidating at first – there’s a lot to ingest within the console. But at the end of the day, it’s just code. I did a cursory reading of Boto3’s documentation tutorial, and then found they had some code examples for DynamoDB. Perfect! Following this, I was able to easily interface my function with Dynamo by defining my TABLE_NAME, and then using the built-in update functions.

At this point, I just needed to make a GET function that retrieved the data from the DB using the table.get_item function, and then call the table.update_item by adding a +1 the value. 
After testing, I was left with an ugly and not easily readable endpoint from API Gateway. Nothing ACM, and Route53 couldn’t fix! I made an ACM certificate for api.cthom.xyz, made the simple route via Route53 A name, and I could now hit my API endpoint publicly with the proper route.

### MOVING BACK TO THE RESUME, INSERT JAVASCRIPT:
 
 ```javascript 

 function updateCounter(){
    fetch('Count',{
        method: 'GET'
    })
  .then(response => {
    if (
        response.ok
    ) {
      return response.json()
    } else {
      throw new Error("Oh no, it's broke!");
    }
  })
  .then(
	data => "You're the 10000th visitor, you're my new best friend.")}
    
```

This is where I decided I needed to add some stylization to my resume. It needs to look and feel pretty! I added a picture of myself (I’m not sure that fits the ‘pretty’ criteria we’re looking for, but we’ll go with it), and stylized the layout. In the footer, I added a JavaScript function fetched the response of my API I built and returned the visitor_count data. It’s looking like we’re getting to the end, but the real fun/challenge has just started: IaC, Source Control, and CI/CD via GitHub Actions.

### ARE WE DEVOPS, YET?:

I decided the approach I would take with the IaC was to work in the same pattern I did through console – start with the Route 53, move on to the bucket, and so on... It just seemed easier to map it out this way, despite it not meaning much as the language is declarative. I decided to go with YAML, because it just looks so comfy. Reading through the whitepapers, I found some pretty neat functions that are supported by CloudFormation - !Ref, !GetAtt, and !Sub. Using these allowed me to reference other resources to build onto another, and since it’s declarative, CloudFormation will just automagically figure it out when deploying. 

I hit plenty of road-bumps along the way – mostly with API Gateway and my custom domain. The only thing I can say with this, is that it is almost ALWAYS user error, or PEBCAK. It was mostly looking over tiny things, and not paying attention to the small details. If you tend to glance over things, CloudFormation will humble you. 
Pro-tip from a casual: If you haven’t heard of [aws-vault](https://github.com/99designs/aws-vault), it made deploying my changes via terminal a breeze. I would also recommend the [VS Code plug-in CloudFormation Linter by kddejong](https://marketplace.visualstudio.com/items?itemName=kddejong.vscode-cfn-lint).

GitHub Actions was something I will admit I wasn’t looking forward to dealing with, despite having Git experience. For some reason, I thought it was going to be much more involved, but to my surprise it’s just YAML! Not only that, but there are also templates out there for pretty much everything out there – no need to reinvent the wheel. I set up a template to move my code to S3 when there was a commit, and then invalidate the CloudFront cache so that my changes are applied instantly. 

![Code Deploy!](https://user-images.githubusercontent.com/7934145/174810233-18ed8295-94f7-4ea7-b18b-f31133463265.png)


### THOUGHTS:
I thoroughly enjoyed the week I spent with the Cloud Resume Challenge. It helped level up my skills in the cloud space – I feel it helped me achieve a grasp of the fundamentals. From here, I would like to continue my studies (looking at you, Cantrill), and get my AWS SAA. I also would like to attempt this challenge within Azure, as I currently am working in a .NET stack. 
I think the greatest part of the Cloud Resume Challenge is that it helped me overcome the fear of the cloud – it’s not as scary as you think, and it’s without a doubt the most fun I’ve had as of recent when it comes to studying.  I also have a number of projects I would like to tackle with AWS – a server-less QR code generator being my next.
