export const SOLNLIMIT = 5;
export const SOLNINITIALOFFSET = 0;

export const subSystems = [
    {
    name : "vision-systems",
    trailer : "videos/smart_solutions/detection.mp4",
    backgroundImage : "images/smart_solutions/EM.jpg",
    position : {x : 0, y : 0},
    subElements : [
        {
        name : "Detection" ,
        short :  "videos/smart_solutions/detection.mp4",
        link : "detection"
        },
        {
        name : "Tracking" ,
        short :  "videos/smart_solutions/tracking.mp4",
        link : "tracking"
        },
        {
        name : "Segmentation" ,
        short :  "videos/smart_solutions/segmentation.mp4",
        link : "segmentation"
        },
    ]
    },
    {
    name : "language-models",
    trailer : "videos/smart_solutions/segmentation.mp4",
    backgroundImage : "images/smart_solutions/EM.jpg",
    position : {x : 0, y : 0},
    subElements : [
        {
        name : "Chat Bot" ,
        short :  "videos/smart_solutions/detection.mp4",
        link : "detection"
        },
        {
        name : "Image Generation" ,
        short :  "videos/smart_solutions/tracking.mp4",
        link : "tracking"
        }
    ]
    },
    {
    name : "time-series-models",
    trailer : "videos/smart_solutions/segmentation.mp4",
    backgroundImage : "images/smart_solutions/EM.jpg",
    position : {x : 0, y : 0},
    subElements : [
        {
        name : "Trading" ,
        short :  "videos/smart_solutions/detection.mp4",
        link : "detection"
        }
    ]
    },
    {
    name : "misc",
    trailer : "videos/smart_solutions/segmentation.mp4",
    backgroundImage : "images/smart_solutions/EM.jpg",
    position : {x : 0, y : 0},
    subElements : [
        {
        name : "Probability" ,
        short :  "videos/smart_solutions/detection.mp4",
        link : "detection"
        }
    ]
    }
]

