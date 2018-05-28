# TurtleCoin-Krang aka Krang

This repo is where a Blockchain Automation Suite is going to live. The end goals are:

1. Completely scripted infrastructure povisioning
   1. 1st Digital Ocean then others Scaleway, Packet, GCE, AWS, etc
2. Completely scripted configuration management
   1. OS updates, Firewalls, IPs, Ports, Software, etc
3. Once the above is developed then combining that to run scenarios
   1. Test a daemon upgrade
   2. Test other daemon implementations
   3. Deploy a complete CI/CD/CD pipeline for TurtleCoin core suite (daemons, wallets, mining pools, etc)
   4. Run benchmarks on the blockchain itself
   5. Run benchmarks on the daemons catching regressions in performance and providing information to identify areas to optimise
4. Web app dashboard 
   1. Eventually we'll get here
   2. An all in one web app that can be used to launch anything above
   3. will provide knobs to turn things up and down
      - deploy 3 daemons to start
      - then add 4 more daemons
      - now add in 6 daemons on the next version
      - now start up wallets and send transactions
   4. will allow for custom scenarios that aren't covered by the existing suite
    
This is the plan. We are going to package everything into Docker containers and as such will build out a Docker build CI/CD/CD pipeline as well. Everything will be automated/scripted.

If you'd like to contribute join us on [#dev_general](https://discord.gg/JutXdZC) on the TurtleCoin Discord server

So far we are:
  + @SoreGums (AU)
  + @Slash-atello (AU)
  + @funkypenguin (NZ)
  
Working Tasklist

Slash-atello Tasks
- Get the 'Terrform Infrastrucure as a code' working and deploying instances to Digital Ocean and AWS (also install ansible requirements)
- Create ansible roles for any complex config managment
- Integrate Docker deployments with funkypenguin (pools, daemons, blockchain explorer etc.)
- Improve the code's readability, portability and reusablity
- SoreGums to review ongoing
      
