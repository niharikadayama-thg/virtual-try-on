// Foundation Shade Finder Application

// Foundation shade database with LAB values
const foundationDatabase = [
    // Fair shades
    {
        brand: "Fenty Beauty",
        name: "Pro Filt'r Soft Matte - 100",
        hex: "#F5E8D3",
        lab: { L: 92.8, a: 1.2, b: 10.5 },
        undertone: "neutral",
        coverage: "medium to full",
        finish: "matte",
        skinToneRange: ["very light"],
        mst: 1 // Monk Skin Tone scale (1-10)
    },
    {
        brand: "Estée Lauder",
        name: "Double Wear - 1C0 Shell",
        hex: "#F2E2D0",
        lab: { L: 90.5, a: 2.8, b: 9.8 },
        undertone: "cool",
        coverage: "full",
        finish: "matte",
        skinToneRange: ["very light"],
        mst: 1
    },
    {
        brand: "MAC Cosmetics",
        name: "Studio Fix Fluid - NC10",
        hex: "#F4E2CD",
        lab: { L: 89.7, a: 3.5, b: 11.2 },
        undertone: "warm",
        coverage: "medium to full",
        finish: "natural matte",
        skinToneRange: ["very light"],
        mst: 1
    },
    
    // Light shades
    {
        brand: "NARS",
        name: "Natural Radiant Longwear - Mont Blanc",
        hex: "#E8D5C0",
        lab: { L: 85.2, a: 4.1, b: 12.8 },
        undertone: "neutral",
        coverage: "medium to full",
        finish: "natural",
        skinToneRange: ["light"],
        mst: 2
    },
    {
        brand: "Maybelline",
        name: "Fit Me Matte - 115 Ivory",
        hex: "#EAD7C0",
        lab: { L: 86.3, a: 3.8, b: 13.5 },
        undertone: "neutral",
        coverage: "medium",
        finish: "matte",
        skinToneRange: ["light"],
        mst: 2
    },
    {
        brand: "L'Oreal",
        name: "True Match - W3 Golden Beige",
        hex: "#E6CEAE",
        lab: { L: 83.5, a: 5.2, b: 18.7 },
        undertone: "warm",
        coverage: "light to medium",
        finish: "natural",
        skinToneRange: ["light"],
        mst: 3
    },
    
    // Medium shades
    {
        brand: "Too Faced",
        name: "Born This Way - Golden Beige",
        hex: "#D8B99A",
        lab: { L: 76.8, a: 8.4, b: 19.5 },
        undertone: "warm",
        coverage: "medium to full",
        finish: "natural",
        skinToneRange: ["medium"],
        mst: 4
    },
    {
        brand: "Fenty Beauty",
        name: "Pro Filt'r Soft Matte - 290",
        hex: "#D4B08E",
        lab: { L: 73.5, a: 9.8, b: 21.2 },
        undertone: "neutral",
        coverage: "medium to full",
        finish: "matte",
        skinToneRange: ["medium"],
        mst: 5
    },
    {
        brand: "Armani Beauty",
        name: "Luminous Silk - 6",
        hex: "#D3B08C",
        lab: { L: 73.2, a: 9.5, b: 22.0 },
        undertone: "neutral",
        coverage: "medium",
        finish: "luminous",
        skinToneRange: ["medium"],
        mst: 5
    },
    
    // Tan shades
    {
        brand: "MAC Cosmetics",
        name: "Studio Fix Fluid - NC42",
        hex: "#C49B76",
        lab: { L: 65.8, a: 11.2, b: 23.5 },
        undertone: "warm",
        coverage: "medium to full",
        finish: "natural matte",
        skinToneRange: ["tan"],
        mst: 6
    },
    {
        brand: "NARS",
        name: "Natural Radiant Longwear - Syracuse",
        hex: "#C19A75",
        lab: { L: 64.5, a: 10.8, b: 22.8 },
        undertone: "warm",
        coverage: "medium to full",
        finish: "natural",
        skinToneRange: ["tan"],
        mst: 6
    },
    {
        brand: "Estée Lauder",
        name: "Double Wear - 4W1 Honey Bronze",
        hex: "#BE9570",
        lab: { L: 62.3, a: 11.5, b: 24.2 },
        undertone: "warm",
        coverage: "full",
        finish: "matte",
        skinToneRange: ["tan"],
        mst: 6
    },
    
    // Deep shades
    {
        brand: "Fenty Beauty",
        name: "Pro Filt'r Soft Matte - 420",
        hex: "#9F7B5A",
        lab: { L: 53.2, a: 12.8, b: 23.5 },
        undertone: "neutral",
        coverage: "medium to full",
        finish: "matte",
        skinToneRange: ["deep"],
        mst: 7
    },
    {
        brand: "Lancôme",
        name: "Teint Idole Ultra - 500 Suede W",
        hex: "#9E7555",
        lab: { L: 51.8, a: 13.5, b: 24.2 },
        undertone: "warm",
        coverage: "full",
        finish: "matte",
        skinToneRange: ["deep"],
        mst: 8
    },
    {
        brand: "MAC Cosmetics",
        name: "Studio Fix Fluid - NW45",
        hex: "#8E5B3F",
        lab: { L: 43.5, a: 15.8, b: 22.5 },
        undertone: "neutral warm",
        coverage: "medium to full",
        finish: "natural matte",
        skinToneRange: ["deep"],
        mst: 8
    },
    
    // Rich shades
    {
        brand: "Fenty Beauty",
        name: "Pro Filt'r Soft Matte - 490",
        hex: "#6C4D3C",
        lab: { L: 35.2, a: 12.5, b: 16.8 },
        undertone: "neutral",
        coverage: "medium to full",
        finish: "matte",
        skinToneRange: ["rich"],
        mst: 9
    },
    {
        brand: "NARS",
        name: "Natural Radiant Longwear - Macao",
        hex: "#6B4A36",
        lab: { L: 34.5, a: 13.2, b: 17.5 },
        undertone: "warm",
        coverage: "medium to full",
        finish: "natural",
        skinToneRange: ["rich"],
        mst: 9
    },
    {
        brand: "Estée Lauder",
        name: "Double Wear - 8N1 Espresso",
        hex: "#5E3D2A",
        lab: { L: 29.8, a: 12.8, b: 15.5 },
        undertone: "neutral",
        coverage: "full",
        finish: "matte",
        skinToneRange: ["rich"],
        mst: 10
    }
];

// Monk Skin Tone Scale (MST) reference
const monkSkinToneScale = [
    { level: 1, name: "Very Light", hex: "#F6EDE4" },
    { level: 2, name: "Light", hex: "#F3E7DB" },
    { level: 3, name: "Light Medium", hex: "#F7DFC4" },
    { level: 4, name: "Medium", hex: "#E5C8A6" },
    { level: 5, name: "Medium Tan", hex: "#D8B390" },
    { level: 6, name: "Tan", hex: "#C99C76" },
    { level: 7, name: "Dark Tan", hex: "#A97955" },
    { level: 8, name: "Deep", hex: "#8D5A3D" },
    { level: 9, name: "Deep Dark", hex: "#674230" },
    { level: 10, name: "Rich", hex: "#483248" }
];

// DOM Elements
const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const skinToneDisplay = document.getElementById('skinToneDisplay');
const skinToneDescription = document.getElementById('skinToneDescription');
const undertoneValue = document.getElementById('undertoneValue');
const recommendationsList = document.getElementById('recommendationsList');

// Variables
let selectedImage = null;
let faceMeshModel = null;

// Initialize MediaPipe FaceMesh
async function initializeModel() {
    try {
        // Load MediaPipe FaceMesh
        faceMeshModel = await faceLandmarksDetection.load(
            faceLandmarksDetection.SupportedPackages.MEDIAPIPE_FACE_MESH,
            { maxFaces: 1 }
        );
        console.log('MediaPipe FaceMesh model loaded successfully');
    } catch (error) {
        console.error('Error loading MediaPipe FaceMesh model:', error);
        alert('Failed to load face detection model. Please try again later.');
    }
}

// Initialize the application
async function init() {
    // Set up event listeners
    setupEventListeners();
    
    // Add face overlay to the upload area
    addFaceOverlay();
    
    // Load MediaPipe model
    await initializeModel();
}

// Add face overlay to guide users
function addFaceOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'face-overlay';
    overlay.innerHTML = `
        <svg width="200" height="240" viewBox="0 0 200 240">
            <ellipse cx="100" cy="120" rx="70" ry="90" stroke="#6a4c93" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
        </svg>
        <p class="overlay-text">Position your face within the oval in good lighting</p>
    `;
    dropArea.appendChild(overlay);
}

// Set up event listeners
function setupEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    dropArea.addEventListener('dragover', handleDragOver);
    dropArea.addEventListener('dragleave', handleDragLeave);
    dropArea.addEventListener('drop', handleDrop);
    dropArea.addEventListener('click', () => fileInput.click());
    
    // Analyze button
    analyzeBtn.addEventListener('click', analyzeFace);
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.type.match('image.*')) {
        processSelectedFile(file);
    }
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    dropArea.classList.add('active');
}

// Handle drag leave
function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    dropArea.classList.remove('active');
}

// Handle drop
function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    dropArea.classList.remove('active');
    
    const file = event.dataTransfer.files[0];
    if (file && file.type.match('image.*')) {
        processSelectedFile(file);
    }
}

// Process the selected file
function processSelectedFile(file) {
    selectedImage = file;
    
    // Create file reader to display preview
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        imagePreview.hidden = false;
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

// Analyze face
async function analyzeFace() {
    if (!selectedImage || !faceMeshModel) {
        return;
    }
    
    try {
        // Show loading state
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing...';
        
        // Create an image element for MediaPipe
        const img = new Image();
        img.src = imagePreview.src;
        
        // Wait for image to load
        await new Promise(resolve => {
            img.onload = resolve;
        });
        
        // Create canvas for image processing
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        
        // Detect face landmarks using MediaPipe FaceMesh
        const predictions = await faceMeshModel.estimateFaces(img);
        
        if (predictions.length === 0) {
            throw new Error('No face detected in the image. Please try another photo with clear lighting and your face centered in the frame.');
        }
        
        // Apply white balance correction (Gray World algorithm)
        const whiteBalancedImageData = applyGrayWorldWhiteBalance(ctx, canvas.width, canvas.height);
        
        // Extract skin tone from face using landmarks
        const skinToneInfo = extractSkinToneFromLandmarks(whiteBalancedImageData, predictions[0], canvas.width);
        
        // Display results
        displayResults(skinToneInfo);
        
        // Reset button state
        analyzeBtn.textContent = 'Analyze Face';
        analyzeBtn.disabled = false;
        
    } catch (error) {
        console.error('Error analyzing face:', error);
        alert(error.message || 'Error analyzing face. Please try again with a clearer photo in good lighting.');
        
        // Reset button state
        analyzeBtn.textContent = 'Analyze Face';
        analyzeBtn.disabled = false;
    }
}

// Apply Gray World white balance algorithm
function applyGrayWorldWhiteBalance(ctx, width, height) {
    // Get image data
    const imageData = ctx.getImageData(0, 0, width, height);
    const data = imageData.data;
    
    // Calculate average RGB
    let avgR = 0, avgG = 0, avgB = 0;
    let pixelCount = 0;
    
    for (let i = 0; i < data.length; i += 4) {
        avgR += data[i];
        avgG += data[i + 1];
        avgB += data[i + 2];
        pixelCount++;
    }
    
    avgR /= pixelCount;
    avgG /= pixelCount;
    avgB /= pixelCount;
    
    // Calculate gray value (average of RGB averages)
    const grayValue = (avgR + avgG + avgB) / 3;
    
    // Calculate scaling factors
    const scaleR = grayValue / avgR;
    const scaleG = grayValue / avgG;
    const scaleB = grayValue / avgB;
    
    // Apply correction
    for (let i = 0; i < data.length; i += 4) {
        data[i] = Math.min(255, data[i] * scaleR);
        data[i + 1] = Math.min(255, data[i + 1] * scaleG);
        data[i + 2] = Math.min(255, data[i + 2] * scaleB);
    }
    
    return imageData;
}

// Extract skin tone from face using MediaPipe landmarks
function extractSkinToneFromLandmarks(imageData, facePrediction, canvasWidth) {
    const data = imageData.data;
    const landmarks = facePrediction.mesh || facePrediction.scaledMesh;
    
    // Define sampling regions using landmark indices
    // MediaPipe Face Mesh has 468 landmarks
    // Reference: https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png
    
    // Cheek regions (left and right)
    const leftCheekIndices = [117, 118, 119, 120, 121, 122, 123, 147, 187, 207, 206, 203, 204];
    const rightCheekIndices = [346, 347, 348, 349, 350, 351, 352, 376, 411, 427, 426, 423, 424];
    
    // Forehead region
    const foreheadIndices = [9, 8, 7, 6, 5, 4, 3, 2, 1, 10, 151, 337, 299, 332, 333, 334, 335, 336];
    
    // Jawline region
    const jawlineIndices = [200, 199, 175, 152, 148, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109];
    
    // Sample pixels from each region
    const leftCheekSamples = sampleRegion(data, landmarks, leftCheekIndices, canvasWidth);
    const rightCheekSamples = sampleRegion(data, landmarks, rightCheekIndices, canvasWidth);
    const foreheadSamples = sampleRegion(data, landmarks, foreheadIndices, canvasWidth);
    const jawlineSamples = sampleRegion(data, landmarks, jawlineIndices, canvasWidth);
    
    // Combine all samples
    const allSamples = [...leftCheekSamples, ...rightCheekSamples, ...foreheadSamples, ...jawlineSamples];
    
    // Convert RGB samples to LAB
    const labSamples = allSamples.map(rgb => rgbToLab(rgb.r, rgb.g, rgb.b));
    
    // Calculate ITA (Individual Typology Angle) for each sample
    const itaValues = labSamples.map(lab => calculateITA(lab));
    
    // Calculate median ITA (more robust than mean)
    const medianITA = calculateMedian(itaValues);
    
    // Determine skin tone category based on ITA
    const skinToneCategory = determineSkinToneCategoryFromITA(medianITA);
    
    // Calculate average LAB values for undertone analysis
    const avgLab = labSamples.reduce((acc, lab) => {
        return {
            L: acc.L + lab.L / labSamples.length,
            a: acc.a + lab.a / labSamples.length,
            b: acc.b + lab.b / labSamples.length
        };
    }, { L: 0, a: 0, b: 0 });
    
    // Determine undertone
    const undertone = determineUndertone(avgLab);
    
    // Convert average LAB back to RGB for display
    const avgRgb = labToRgb(avgLab.L, avgLab.a, avgLab.b);
    const hexColor = rgbToHex(avgRgb.r, avgRgb.g, avgRgb.b);
    
    // Map to Monk Skin Tone scale
    const mstLevel = mapToMonkSkinTone(avgLab);
    
    return {
        color: hexColor,
        lab: avgLab,
        ita: medianITA,
        category: skinToneCategory,
        undertone: undertone,
        mst: mstLevel
    };
}

// Sample pixels from a region defined by landmark indices
function sampleRegion(imageData, landmarks, landmarkIndices, canvasWidth) {
    const samples = [];
    
    // For each landmark in the region
    for (const idx of landmarkIndices) {
        const landmark = landmarks[idx];
        const x = Math.round(landmark[0]);
        const y = Math.round(landmark[1]);
        
        // Get pixel at landmark position
        const pixelIndex = (y * canvasWidth + x) * 4;
        
        // Only add valid pixels
        if (pixelIndex >= 0 && pixelIndex < imageData.length - 3) {
            samples.push({
                r: imageData[pixelIndex],
                g: imageData[pixelIndex + 1],
                b: imageData[pixelIndex + 2]
            });
        }
    }
    
    return samples;
}

// Calculate ITA (Individual Typology Angle)
function calculateITA(lab) {
    // ITA° = arctan((L*−50)/b*) * 180/π
    return Math.atan((lab.L - 50) / lab.b) * (180 / Math.PI);
}

// Calculate median of an array
function calculateMedian(values) {
    const sorted = [...values].sort((a, b) => a - b);
    const middle = Math.floor(sorted.length / 2);
    
    if (sorted.length % 2 === 0) {
        return (sorted[middle - 1] + sorted[middle]) / 2;
    }
    
    return sorted[middle];
}

// Determine skin tone category from ITA value
function determineSkinToneCategoryFromITA(ita) {
    // ITA ranges based on standard classifications
    if (ita > 55) {
        return { name: "very light", description: "Very Light skin tone" };
    } else if (ita > 41) {
        return { name: "light", description: "Light skin tone" };
    } else if (ita > 28) {
        return { name: "intermediate", description: "Intermediate skin tone" };
    } else if (ita > 10) {
        return { name: "tan", description: "Tan skin tone" };
    } else if (ita > -30) {
        return { name: "brown", description: "Brown skin tone" };
    } else {
        return { name: "dark", description: "Dark skin tone" };
    }
}

// Determine undertone from LAB values
function determineUndertone(lab) {
    // Calculate hue angle in the a*b* plane
    const hueAngle = Math.atan2(lab.b, lab.a) * (180 / Math.PI);
    
    // Analyze a* and b* values for undertone
    // Higher a* (redness) relative to b* (yellowness) suggests warm undertone
    // Higher b* relative to a* suggests cool undertone
    
    if (lab.a > lab.b * 0.9) {
        return "warm";
    } else if (lab.b > lab.a * 1.5) {
        return "cool";
    } else {
        return "neutral";
    }
}

// Map LAB values to Monk Skin Tone scale (1-10)
function mapToMonkSkinTone(lab) {
    // Convert MST hex colors to LAB
    const mstLabValues = monkSkinToneScale.map(tone => {
        const rgb = hexToRgb(tone.hex);
        return {
            level: tone.level,
            lab: rgbToLab(rgb.r, rgb.g, rgb.b)
        };
    });
    
    // Find closest MST level by calculating color distance in LAB space
    let closestLevel = 1;
    let minDistance = Number.MAX_VALUE;
    
    for (const mst of mstLabValues) {
        const distance = calculateLabDistance(lab, mst.lab);
        if (distance < minDistance) {
            minDistance = distance;
            closestLevel = mst.level;
        }
    }
    
    return closestLevel;
}

// Calculate Euclidean distance in LAB space
function calculateLabDistance(lab1, lab2) {
    return Math.sqrt(
        Math.pow(lab1.L - lab2.L, 2) +
        Math.pow(lab1.a - lab2.a, 2) +
        Math.pow(lab1.b - lab2.b, 2)
    );
}

// Calculate color difference using CIEDE2000 (simplified version)
function calculateColorDifference(lab1, lab2) {
    // Simplified CIEDE2000 implementation
    // For a full implementation, consider using a color science library
    
    // Calculate differences
    const deltaL = lab1.L - lab2.L;
    const deltaA = lab1.a - lab2.a;
    const deltaB = lab1.b - lab2.b;
    
    // Calculate Euclidean distance (simplified)
    return Math.sqrt(deltaL * deltaL + deltaA * deltaA + deltaB * deltaB);
}

// Display results
function displayResults(skinToneInfo) {
    // Display skin tone color
    skinToneDisplay.style.backgroundColor = skinToneInfo.color;
    
    // Display skin tone description
    skinToneDescription.textContent = `${skinToneInfo.category.description} (MST Level: ${skinToneInfo.mst})`;
    
    // Display undertone
    undertoneValue.textContent = capitalizeFirstLetter(skinToneInfo.undertone);
    
    // Get foundation recommendations
    const recommendations = getFoundationRecommendations(skinToneInfo);
    
    // Display recommendations
    displayRecommendations(recommendations);
    
    // Show results section
    resultsSection.hidden = false;
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Get foundation recommendations
function getFoundationRecommendations(skinToneInfo) {
    // Filter foundations by MST level (allow +/- 1 level)
    let matches = foundationDatabase.filter(foundation => 
        Math.abs(foundation.mst - skinToneInfo.mst) <= 1
    );
    
    // Sort by color similarity using LAB values
    matches.sort((a, b) => {
        const distanceA = calculateColorDifference(a.lab, skinToneInfo.lab);
        const distanceB = calculateColorDifference(b.lab, skinToneInfo.lab);
        
        // Prioritize undertone match
        if (a.undertone === skinToneInfo.undertone && b.undertone !== skinToneInfo.undertone) {
            return -1;
        }
        if (b.undertone === skinToneInfo.undertone && a.undertone !== skinToneInfo.undertone) {
            return 1;
        }
        
        // If undertone is the same or both different, sort by color distance
        return distanceA - distanceB;
    });
    
    // Return top 6 matches
    return matches.slice(0, 6);
}

// Display recommendations
function displayRecommendations(recommendations) {
    // Clear previous recommendations
    recommendationsList.innerHTML = '';
    
    // Add each recommendation
    recommendations.forEach(foundation => {
        const card = document.createElement('div');
        card.className = 'foundation-card';
        
        const colorDiv = document.createElement('div');
        colorDiv.className = 'foundation-color';
        colorDiv.style.backgroundColor = foundation.hex;
        
        const infoDiv = document.createElement('div');
        infoDiv.className = 'foundation-info';
        
        const brandName = document.createElement('h4');
        brandName.textContent = foundation.brand;
        
        const foundationName = document.createElement('p');
        foundationName.textContent = foundation.name;
        
        const foundationDetails = document.createElement('p');
        foundationDetails.textContent = `${capitalizeFirstLetter(foundation.coverage)}, ${foundation.finish} finish`;
        
        const undertoneTag = document.createElement('span');
        undertoneTag.className = 'undertone-tag';
        undertoneTag.textContent = capitalizeFirstLetter(foundation.undertone);
        
        infoDiv.appendChild(brandName);
        infoDiv.appendChild(foundationName);
        infoDiv.appendChild(foundationDetails);
        infoDiv.appendChild(undertoneTag);
        
        card.appendChild(colorDiv);
        card.appendChild(infoDiv);
        
        recommendationsList.appendChild(card);
    });
    
    // Add user feedback controls
    addUserFeedbackControls();
}

// Add user feedback controls
function addUserFeedbackControls() {
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'feedback-controls';
    
    const feedbackHeading = document.createElement('h3');
    feedbackHeading.textContent = 'Adjust Results';
    
    const lighterBtn = document.createElement('button');
    lighterBtn.className = 'feedback-btn';
    lighterBtn.textContent = 'Lighter';
    
    const darkerBtn = document.createElement('button');
    darkerBtn.className = 'feedback-btn';
    darkerBtn.textContent = 'Darker';
    
    const warmerBtn = document.createElement('button');
    warmerBtn.className = 'feedback-btn';
    warmerBtn.textContent = 'Warmer';
    
    const coolerBtn = document.createElement('button');
    coolerBtn.className = 'feedback-btn';
    coolerBtn.textContent = 'Cooler';
    
    const neutralBtn = document.createElement('button');
    neutralBtn.className = 'feedback-btn';
    neutralBtn.textContent = 'More Neutral';
    
    // Add event listeners for feedback buttons
    lighterBtn.addEventListener('click', () => adjustRecommendations('lighter'));
    darkerBtn.addEventListener('click', () => adjustRecommendations('darker'));
    warmerBtn.addEventListener('click', () => adjustRecommendations('warmer'));
    coolerBtn.addEventListener('click', () => adjustRecommendations('cooler'));
    neutralBtn.addEventListener('click', () => adjustRecommendations('neutral'));
    
    // Create button container
    const btnContainer = document.createElement('div');
    btnContainer.className = 'feedback-btn-container';
    
    // Add buttons to container
    btnContainer.appendChild(lighterBtn);
    btnContainer.appendChild(darkerBtn);
    btnContainer.appendChild(warmerBtn);
    btnContainer.appendChild(coolerBtn);
    btnContainer.appendChild(neutralBtn);
    
    // Add heading and buttons to feedback div
    feedbackDiv.appendChild(feedbackHeading);
    feedbackDiv.appendChild(btnContainer);
    
    // Add feedback div to recommendations section
    recommendationsList.parentNode.appendChild(feedbackDiv);
}

// Adjust recommendations based on user feedback
function adjustRecommendations(adjustment) {
    // Get current skin tone info from display
    const currentColor = skinToneDisplay.style.backgroundColor;
    const rgb = parseRGB(currentColor);
    const lab = rgbToLab(rgb.r, rgb.g, rgb.b);
    
    // Adjust LAB values based on feedback
    let adjustedLab = { ...lab };
    
    switch (adjustment) {
        case 'lighter':
            adjustedLab.L = Math.min(100, lab.L + 5);
            break;
        case 'darker':
            adjustedLab.L = Math.max(0, lab.L - 5);
            break;
        case 'warmer':
            adjustedLab.a = Math.min(128, lab.a + 3);
            break;
        case 'cooler':
            adjustedLab.b = Math.min(128, lab.b + 3);
            break;
        case 'neutral':
            // Move a and b values closer to neutral
            adjustedLab.a = lab.a * 0.8;
            adjustedLab.b = lab.b * 0.8;
            break;
    }
    
    // Recalculate ITA
    const adjustedITA = calculateITA(adjustedLab);
    
    // Update skin tone category
    const adjustedCategory = determineSkinToneCategoryFromITA(adjustedITA);
    
    // Update undertone
    const adjustedUndertone = determineUndertone(adjustedLab);
    
    // Convert back to RGB for display
    const adjustedRgb = labToRgb(adjustedLab.L, adjustedLab.a, adjustedLab.b);
    const adjustedHex = rgbToHex(adjustedRgb.r, adjustedRgb.g, adjustedRgb.b);
    
    // Map to MST
    const adjustedMST = mapToMonkSkinTone(adjustedLab);
    
    // Create adjusted skin tone info
    const adjustedSkinToneInfo = {
        color: adjustedHex,
        lab: adjustedLab,
        ita: adjustedITA,
        category: adjustedCategory,
        undertone: adjustedUndertone,
        mst: adjustedMST
    };
    
    // Update display
    skinToneDisplay.style.backgroundColor = adjustedHex;
    skinToneDescription.textContent = `${adjustedCategory.description} (MST Level: ${adjustedMST})`;
    undertoneValue.textContent = capitalizeFirstLetter(adjustedUndertone);
    
    // Get new recommendations
    const newRecommendations = getFoundationRecommendations(adjustedSkinToneInfo);
    
    // Update recommendations display (without feedback controls)
    recommendationsList.innerHTML = '';
    newRecommendations.forEach(foundation => {
        const card = document.createElement('div');
        card.className = 'foundation-card';
        
        const colorDiv = document.createElement('div');
        colorDiv.className = 'foundation-color';
        colorDiv.style.backgroundColor = foundation.hex;
        
        const infoDiv = document.createElement('div');
        infoDiv.className = 'foundation-info';
        
        const brandName = document.createElement('h4');
        brandName.textContent = foundation.brand;
        
        const foundationName = document.createElement('p');
        foundationName.textContent = foundation.name;
        
        const foundationDetails = document.createElement('p');
        foundationDetails.textContent = `${capitalizeFirstLetter(foundation.coverage)}, ${foundation.finish} finish`;
        
        const undertoneTag = document.createElement('span');
        undertoneTag.className = 'undertone-tag';
        undertoneTag.textContent = capitalizeFirstLetter(foundation.undertone);
        
        infoDiv.appendChild(brandName);
        infoDiv.appendChild(foundationName);
        infoDiv.appendChild(foundationDetails);
        infoDiv.appendChild(undertoneTag);
        
        card.appendChild(colorDiv);
        card.appendChild(infoDiv);
        
        recommendationsList.appendChild(card);
    });
    
    // Log user feedback for improvement
    console.log(`User adjusted results: ${adjustment}`, adjustedSkinToneInfo);
}

// Parse RGB from CSS backgroundColor
function parseRGB(rgbString) {
    const matches = rgbString.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (matches) {
        return {
            r: parseInt(matches[1]),
            g: parseInt(matches[2]),
            b: parseInt(matches[3])
        };
    }
    return { r: 0, g: 0, b: 0 };
}

// Convert RGB to LAB color space
function rgbToLab(r, g, bValue) {
    // First, normalize RGB values
    r = r / 255;
    g = g / 255;
    let bNorm = bValue / 255;
    
    // Apply gamma correction
    r = (r > 0.04045) ? Math.pow((r + 0.055) / 1.055, 2.4) : r / 12.92;
    g = (g > 0.04045) ? Math.pow((g + 0.055) / 1.055, 2.4) : g / 12.92;
    bNorm = (bNorm > 0.04045) ? Math.pow((bNorm + 0.055) / 1.055, 2.4) : bNorm / 12.92;
    
    // Convert to XYZ
    const x = r * 0.4124 + g * 0.3576 + bNorm * 0.1805;
    const y = r * 0.2126 + g * 0.7152 + bNorm * 0.0722;
    const z = r * 0.0193 + g * 0.1192 + bNorm * 0.9505;
    
    // Convert XYZ to Lab
    // Reference values for D65 illuminant
    const xRef = 0.95047;
    const yRef = 1.0;
    const zRef = 1.08883;
    
    const xNorm = x / xRef;
    const yNorm = y / yRef;
    const zNorm = z / zRef;
    
    const fx = (xNorm > 0.008856) ? Math.pow(xNorm, 1/3) : (7.787 * xNorm) + (16/116);
    const fy = (yNorm > 0.008856) ? Math.pow(yNorm, 1/3) : (7.787 * yNorm) + (16/116);
    const fz = (zNorm > 0.008856) ? Math.pow(zNorm, 1/3) : (7.787 * zNorm) + (16/116);
    
    const L = (116 * fy) - 16;
    const a = 500 * (fx - fy);
    const b = 200 * (fy - fz);
    
    return { L, a, b };
}

// Convert LAB to RGB color space
function labToRgb(L, a, bValue) {
    // Convert Lab to XYZ
    const fy = (L + 16) / 116;
    const fx = a / 500 + fy;
    const fz = fy - bValue / 200;
    
    // Reference values for D65 illuminant
    const xRef = 0.95047;
    const yRef = 1.0;
    const zRef = 1.08883;
    
    const xNorm = (Math.pow(fx, 3) > 0.008856) ? Math.pow(fx, 3) : (fx - 16/116) / 7.787;
    const yNorm = (Math.pow(fy, 3) > 0.008856) ? Math.pow(fy, 3) : (fy - 16/116) / 7.787;
    const zNorm = (Math.pow(fz, 3) > 0.008856) ? Math.pow(fz, 3) : (fz - 16/116) / 7.787;
    
    const x = xNorm * xRef;
    const y = yNorm * yRef;
    const z = zNorm * zRef;
    
    // Convert XYZ to RGB
    let r = x * 3.2406 + y * -1.5372 + z * -0.4986;
    let g = x * -0.9689 + y * 1.8758 + z * 0.0415;
    let bVal = x * 0.0557 + y * -0.2040 + z * 1.0570;
    
    // Apply gamma correction
    r = (r > 0.0031308) ? 1.055 * Math.pow(r, 1/2.4) - 0.055 : 12.92 * r;
    g = (g > 0.0031308) ? 1.055 * Math.pow(g, 1/2.4) - 0.055 : 12.92 * g;
    bVal = (bVal > 0.0031308) ? 1.055 * Math.pow(bVal, 1/2.4) - 0.055 : 12.92 * bVal;
    
    // Normalize and clamp RGB values
    r = Math.max(0, Math.min(1, r)) * 255;
    g = Math.max(0, Math.min(1, g)) * 255;
    bVal = Math.max(0, Math.min(1, bVal)) * 255;
    
    return {
        r: Math.round(r),
        g: Math.round(g),
        b: Math.round(bVal)
    };
}

// Convert RGB to HEX
function rgbToHex(r, g, b) {
    return '#' + [r, g, b].map(x => {
        const hex = Math.round(x).toString(16);
        return hex.length === 1 ? '0' + hex : hex;
    }).join('');
}

// Convert HEX to RGB
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
}

// Capitalize first letter of a string
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Initialize the application when the page loads
window.addEventListener('DOMContentLoaded', init);