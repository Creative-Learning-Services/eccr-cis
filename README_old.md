# ECCR-CIS

## ECCR System Architecture

```mermaid
---
config:
        layout: elk
title: ECCR Connected Systems
---
graph TD;
        subgraph Legend
                1("System")-->|MVP|2("System");
                1("System")-.->|Future Planned|2("System");
        end
        subgraph External
                LDSS;
                XIA;
                ECC;
                ELRR;
                EDLM[EDLM Portal];
        end
        subgraph ECCR
                CIS;
                CES;
                CDS;
                CMS;
                CDSUI[CDS UI];
                CMSUI[CMS UI];
        end
        LDSS-->|Profile|CIS;
        XIA-.->|Indexing|CIS;
        CIS-.->|References|ECC & ELRR & EDLM;
        CIS-->|Competency & Credential|CMS;
        CIS-.->|Competency & Credential|CDS & CES;
        CMS-->CMSUI;
        CDS-.->CDSUI;
        CES-.->CDS;
```

## ECCR Data Diagram

### DOT&E Domain Diagram

![ECCR DOT&E Domain Diagram](./assets/DOT&E_Graph.png)

### DCWF Domain Diagram

![DCWF Domain Diagram](./assets/DCWF_GRAPH_MODEL.png)
