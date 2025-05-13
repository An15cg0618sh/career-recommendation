document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const careerForm = document.getElementById('careerForm');
    
    if (careerForm) {
        careerForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Skills validation - at least 3 required
            const selectedSkills = document.querySelectorAll('input[name="skills"]:checked');
            const skillsValidation = document.getElementById('skills-validation');
            
            if (selectedSkills.length < 3) {
                skillsValidation.textContent = 'Please select at least 3 skills.';
                isValid = false;
            } else {
                skillsValidation.textContent = '';
            }
            
            // Interests validation - at least 2 required
            const selectedInterests = document.querySelectorAll('input[name="interests"]:checked');
            const interestsValidation = document.getElementById('interests-validation');
            
            if (selectedInterests.length < 2) {
                interestsValidation.textContent = 'Please select at least 2 interests.';
                isValid = false;
            } else {
                interestsValidation.textContent = '';
            }
            
            // Education validation - one option required
            const selectedEducation = document.querySelector('input[name="education"]:checked');
            const educationValidation = document.getElementById('education-validation');
            
            if (!selectedEducation) {
                educationValidation.textContent = 'Please select your education level.';
                isValid = false;
            } else {
                educationValidation.textContent = '';
            }
            
            // Prevent form submission if validation fails
            if (!isValid) {
                e.preventDefault();
                
                // Scroll to the first validation error
                const firstError = document.querySelector('.validation-message:not(:empty)');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
        
        // Reset validation messages when form is reset
        careerForm.addEventListener('reset', function() {
            const validationMessages = document.querySelectorAll('.validation-message');
            validationMessages.forEach(message => {
                message.textContent = '';
            });
        });
    }
    
    // Animated progress circles in results page
    const circles = document.querySelectorAll('.circle');
    
    if (circles.length > 0) {
        // Delay animation slightly for visual effect
        setTimeout(() => {
            circles.forEach(circle => {
                const value = circle.getAttribute('stroke-dasharray').split(',')[0];
                circle.style.strokeDasharray = '0, 100';
                
                setTimeout(() => {
                    circle.style.strokeDasharray = `${value}, 100`;
                }, 300);
            });
        }, 500);
    }
    
    // Add highlighting effect to matching skills and education
    const matchItems = document.querySelectorAll('.match');
    
    if (matchItems.length > 0) {
        matchItems.forEach(item => {
            item.style.transition = 'all 0.5s ease';
        });
    }
});