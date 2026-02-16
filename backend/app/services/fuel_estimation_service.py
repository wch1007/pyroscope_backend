"""
Fuel Load Estimation Service using Selenium WebDriver
Automates interaction with https://fe.wildlands.ai/
"""
import os
import time
import logging
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from app.config import settings

logger = logging.getLogger(__name__)


class FuelEstimationService:
    """Service for estimating fuel load using Wildlands AI web interface"""
    
    def __init__(self):
        self.api_url = settings.FUEL_ESTIMATION_API_URL
        self.timeout = settings.FUEL_ESTIMATION_TIMEOUT
        self.headless = settings.FUEL_ESTIMATION_HEADLESS
        self.driver = None
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Setup and configure Chrome WebDriver"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless=new")
            
            # Additional options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # Use webdriver-manager to handle ChromeDriver installation
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            logger.info("Chrome WebDriver initialized successfully")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
            raise RuntimeError(f"WebDriver initialization failed: {str(e)}")
    
    def _parse_result_text(self, text: str) -> Optional[float]:
        """
        Parse result text to extract numeric value
        Example: "0.165 tons/acre" -> 0.165
        """
        try:
            # Extract the first number from the text
            parts = text.strip().split()
            for part in parts:
                try:
                    return float(part)
                except ValueError:
                    continue
            return None
        except Exception as e:
            logger.warning(f"Failed to parse result text '{text}': {str(e)}")
            return None
    
    def estimate_fuel_load(self, image_path: str) -> Dict[str, any]:
        """
        Estimate fuel load from an image file
        
        Args:
            image_path: Absolute path to the image file
            
        Returns:
            Dictionary containing fuel estimation results:
            {
                "success": bool,
                "total_fuel_load": float,  # tons/acre
                "one_hour_fuel": float,    # tons/acre
                "ten_hour_fuel": float,    # tons/acre
                "hundred_hour_fuel": float, # tons/acre
                "pine_cone_count": int,
                "error": str (optional)
            }
        """
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"Image file not found: {image_path}"
            }
        
        try:
            # Initialize WebDriver
            self.driver = self._setup_driver()
            
            # Navigate to the website
            logger.info(f"Navigating to {self.api_url}")
            self.driver.get(self.api_url)
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, self.timeout)
            
            # Find and interact with file input
            logger.info("Looking for file input element")
            file_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            # Upload the image
            logger.info(f"Uploading image: {image_path}")
            file_input.send_keys(os.path.abspath(image_path))
            
            # Wait a moment for file to be processed
            time.sleep(1)
            
            # Find and click the "Get Fuel Estimate" button
            logger.info("Looking for submit button")
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get Fuel Estimate')]"))
            )
            
            logger.info("Clicking submit button")
            submit_button.click()
            
            # Wait for results to appear
            logger.info("Waiting for results...")
            time.sleep(3)  # Initial wait for processing
            
            # Try to find result elements with different possible selectors
            result_selectors = [
                (By.XPATH, "//div[contains(text(), 'Fuel Estimates Total')]"),
                (By.XPATH, "//*[contains(text(), 'tons/acre')]"),
                (By.CLASS_NAME, "result"),
                (By.ID, "result"),
            ]
            
            results_found = False
            for selector_type, selector_value in result_selectors:
                try:
                    wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                    results_found = True
                    logger.info(f"Results found using selector: {selector_type}={selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if not results_found:
                # Wait longer and try to get any visible text
                time.sleep(5)
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                logger.warning(f"Results not found with known selectors. Page text: {page_text[:500]}")
            
            # Extract results from the page
            # Try multiple approaches to find the results
            results = self._extract_results()
            
            logger.info(f"Fuel estimation completed successfully: {results}")
            return results
            
        except TimeoutException as e:
            error_msg = f"Timeout waiting for elements: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        
        except WebDriverException as e:
            error_msg = f"WebDriver error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        
        except Exception as e:
            error_msg = f"Unexpected error during fuel estimation: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        
        finally:
            # Clean up
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("WebDriver closed successfully")
                except Exception as e:
                    logger.warning(f"Error closing WebDriver: {str(e)}")
                self.driver = None
    
    def _extract_results(self) -> Dict[str, any]:
        """Extract fuel estimation results from the page"""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"Extracting results from page text: {page_text[:500]}")
            
            results = {
                "success": True,
                "total_fuel_load": None,
                "one_hour_fuel": None,
                "ten_hour_fuel": None,
                "hundred_hour_fuel": None,
                "pine_cone_count": None,
            }
            
            # Parse the page text to extract values
            lines = page_text.split('\n')
            
            for line in lines:
                line_lower = line.lower()
                
                if 'fuel estimates total' in line_lower and 'tons/acre' in line_lower:
                    results["total_fuel_load"] = self._parse_result_text(line)
                
                elif 'estimated one hour fuel' in line_lower and 'tons/acre' in line_lower:
                    results["one_hour_fuel"] = self._parse_result_text(line)
                
                elif 'estimated ten hour fuel' in line_lower and 'tons/acre' in line_lower:
                    results["ten_hour_fuel"] = self._parse_result_text(line)
                
                elif 'estimated hundred hour fuel' in line_lower and 'tons/acre' in line_lower:
                    results["hundred_hour_fuel"] = self._parse_result_text(line)
                
                elif 'estimated count of pine cones' in line_lower:
                    count_str = line.split()[-1]
                    try:
                        results["pine_cone_count"] = int(count_str)
                    except ValueError:
                        logger.warning(f"Failed to parse pine cone count: {count_str}")
            
            # Validate that we got at least the total fuel load
            if results["total_fuel_load"] is None:
                logger.warning("Failed to extract total fuel load from results")
                results["success"] = False
                results["error"] = "Failed to parse fuel estimation results"
            
            return results
            
        except Exception as e:
            logger.error(f"Error extracting results: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to extract results: {str(e)}"
            }
    
    async def estimate_fuel_load_async(self, image_path: str) -> Dict[str, any]:
        """
        Async wrapper for fuel load estimation
        Can be extended to run in a thread pool if needed
        """
        # For now, just call the sync version
        # In production, you might want to use asyncio.to_thread() or a task queue
        return self.estimate_fuel_load(image_path)
