#!/bin/bash

# Create main directories
mkdir -p rfp_responses/{openshift,rancher,hardware}/{customer1,customer2,customer3}

# Function to generate random technical terms
generate_tech_term() {
    local terms=("PowerEdge R750" "OpenShift 4.12" "SUSE Rancher 2.7" "Kubernetes" "containerization" 
                "microservices" "CI/CD pipeline" "GitOps" "infrastructure-as-code" "bare metal" 
                "hyperconverged" "multi-cloud" "edge computing" "service mesh" "persistent storage")
    echo "${terms[$RANDOM % ${#terms[@]}]}"
}

# Generate quirky questions and answers
generate_content() {
    local questions=(
        "# How many PowerEdge servers do we need to host a digital petting zoo for containerized applications?\nBased on our analysis of your virtual animal workloads, you'll need 42 PowerEdge R750 servers. This accounts for the resource requirements of 1,000 containerized kittens, 500 virtualized puppies, and one particularly demanding digital elephant that insists on running legacy COBOL applications.\n\nThe solution includes:\n- High-availability treats distribution system\n- Virtual belly-rub scheduler\n- Automated yarn ball deployment pipeline"

        "# Can OpenShift clusters experience separation anxiety?\nYes, OpenShift clusters can develop separation anxiety if nodes are removed without proper farewell ceremonies. Our solution implements a proprietary 'Node Therapy' system that includes:\n\n- Mandatory group hugs between worker nodes\n- Daily affirmation broadcasts to the control plane\n- Emergency comfort container deployment\n- Specialized pod counseling services"

        "# What's the optimal temperature for SUSE Rancher servers if they're feeling under the weather?\nOur comprehensive analysis shows that Rancher servers perform best at exactly 20.42°C when they're feeling poorly. We recommend:\n\n- Installing digital thermometers with emoji support\n- Implementing a chicken soup delivery pipeline\n- Deploying comfort containers with virtual blankets\n- Setting up automated get-well-soon message broadcasts"

        "# How do we ensure our containers don't get lonely during off-peak hours?\nOur innovative solution includes a comprehensive Container Companionship Program™:\n\n- Automated pod playdate scheduling\n- Virtual water cooler spaces for social containers\n- Late-night container karaoke sessions\n- Emergency deployment of companion containers for emotional support"

        "# What's the best way to migrate legacy applications that are afraid of the cloud?\nOur gentle cloud migration strategy includes:\n\n- Progressive exposure therapy to containerization\n- Soothing migration mantras played over the network\n- Comfort zones with familiar monolithic architecture\n- Gradual introduction to microservices through friendship programs"

        "# How many DevOps engineers does it take to debug a self-aware Kubernetes cluster?\nBased on our experience with sentient infrastructure, you'll need:\n\n- 3 DevOps therapists\n- 1 Kubernetes whisperer\n- 2 container psychologists\n- 1 on-call philosopher for existential crises"

        "# Can we implement a happiness monitoring system for our OpenShift nodes?\nOur proposed solution includes:\n\n- Real-time node mood tracking\n- Automated joke delivery to stressed pods\n- Regular virtual team building exercises\n- Emergency deployment of digital comfort food"

        "# What's the recommended approach for handling containers with imposter syndrome?\nOur container confidence-building program includes:\n\n- Daily container affirmation broadcasts\n- Peer support groups for insecure microservices\n- Achievement sticker system for successful deployments\n- Professional development workshops for ambitious pods"
    )
    echo "${questions[$RANDOM % ${#questions[@]}]}"
}

# Generate files
for platform in openshift rancher hardware; do
    for customer in customer1 customer2 customer3; do
        # Generate 5 files per customer per platform
        for i in {1..5}; do
            filename="rfp_responses/${platform}/${customer}/query_${i}.md"
            generate_content > "$filename"
            echo "Generated $filename"
        done
    done
done

echo "Generation complete! Created RFP response files with technical whimsy."
