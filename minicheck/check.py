import traceback
import sys 
import time 

from colorama import init, Fore,  Style

init(autoreset=True)

class Check:
    
    '''
    MiniCheck: A minimal python testing framework.
    
    Usage:
        - create a subclass of Check.
        - define test methods with `test_`.
        - use assertion methods (equal, true, false) inside your test script.
        - optionally define setup() and teardown() methods for test preparation and cleanup.
        - call run() method to execute all test cases.
        
    Methods:
        - equal(actual, expected): check if actual and expected value are equal
        - true(exp): check if expression is true.
        - false(exp): check if expression is false.
        - raises(exc_type, func, *args, **kwargs): check if function raises expected exception.
        - run(): run all test methods and print results.
    '''
    
    def __init__(self, delay=1):
        
        ''' initialize the number of case status and loading delay '''
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.delay =  delay
        
        # --- CLI flags to filter test cases by name ---
        self.args = sys.argv[1:]
        self.filter_test = None 
        self.list_tests = False
        
        self._parse_arguments()
        
    def _progress(self, current):
        
        ''' progress bar for testing each cases '''
        
        bar_length = 30
        filled = int(bar_length * current / self.total)
        bar = '=' * filled + '-' * (bar_length - filled)
        
        print(f'\r{Fore.LIGHTBLUE_EX}[{bar}] {current}/{self.total}', end='')
    
    def _loading(self, message='Checking'):
        
        ''' loading animation for testing each cases '''
        
        for index in range(self.delay):
            sys.stdout.write(f'\r{Fore.YELLOW}{message}{'...' * ((index % 3) + 1)} ')
            sys.stdout.flush()
            
            time.sleep(1)
            
        sys.stdout.write('\r' + ' ' * (len(message) + 5) + '\r')
        
    def _help(self):
        
        ''' display help message for CLI usage '''
        
        print(f'''
{Fore.LIGHTMAGENTA_EX}MiniCheck Testing Framework (CLI usage){Style.RESET_ALL}

python test_app.py [options] [filter]

Options:

    -h, --help        Show this help message.
    --list            List all available test methods.
    filter            Run only test methods that contain the filter string in their name. 
    
Examples:

    python test_app.py                   Run all test methods.
    python test_app.py --list            List all available test methods.
    python test_app.py add               Run only test methods with 'add' in their name.        
            ''')
        
    def _parse_arguments(self):
        
        ''' parse command line arguments for tests filtering '''
        
        if '--help' in self.args or '-h' in self.args:
            self._help()
            sys.exit(0)
            
        if '--list' in self.args: self.list_tests = True
        
        for arg in self.args:
            if not arg.startswith('--'):
                self.filter_test = arg
                break
            
    def _test_cases(self):
        return [
            name for name in dir(self)
            if name.startswith('test_')
            and (self.filter_test is None or self.filter_test in name)
        ]
            
    def run(self):
        
        ''' run all test methods in the subclass with `test_` prefix and print results '''
        
        test_case = self._test_cases()
        self.total = len(test_case)
        
        
        if self.list_tests:
            print(f'{Fore.LIGHTMAGENTA_EX}\n---------- Discovered Tests ----------\n{Style.RESET_ALL}')

            for test in test_case:
                print(f'{Fore.LIGHTYELLOW_EX}> {test}{Style.RESET_ALL}')
                
            return
                
        if self.total == 0:
            print(f'{Fore.YELLOW}No tests matched filter{Style.RESET_ALL}')
            return
        
    
        print(f'{Fore.LIGHTMAGENTA_EX}\n---------- Running {self.total} Tests ----------\n{Style.RESET_ALL}')
        
        for index, name in enumerate(test_case, start=1):
            
            start_time = time.time()
            
            try:
                
                self._loading(f'> Check {name}')
                
                ''' prepare before each test case if setup method is defined '''
                if hasattr(self, 'setup'):
                    self.setup()
                
                getattr(self, name)()
                duration = time.time() - start_time
                self.passed += 1
                print(f'{Fore.GREEN}+ {name} PASSED ({duration:.3f}s){Style.RESET_ALL}')
                
                
                ''' clean up after each test case if teardown method is defined '''
                if hasattr(self, 'teardown'):
                    self.teardown()
                    
            except Exception as e:
                
                duration = time.time() - start_time
                self.failed += 1
                print(f'{Fore.RED}- {name} FAILED ({duration:.3f}s){Style.RESET_ALL}')
                traceback.print_exc()
                
            self._progress(index)
            print()
                
        
        print(f'\nSummary >> Passed: {Fore.GREEN}{self.passed}{Style.RESET_ALL}, Failed: {Fore.RED}{self.failed}{Style.RESET_ALL}, Total: {Fore.LIGHTBLUE_EX}{self.total}{Style.RESET_ALL}\n')
        
    # --- assertion methods (helper functions) ---
    # these methods can be used inside test methods
    # basic assertions for testing conditions
    
    def equal(self, actual, expected, message=None):
        if actual != expected: raise AssertionError(message or f'Expected {expected}, got {actual}')
        
    def true(self, expression, message=None):
        if not expression: raise AssertionError(message or f'Expected True, got {expression}')
    
    def false(self, expression, message=None):
        if expression: raise AssertionError(message or f'Expected False, got {expression}')
        
    def raises(self, exception_type, func, *args, **kwargs):
        try: func(*args, **kwargs)
        except Exception: return 
        except Exception as e: raise AssertionError(f'Expected exception {exception_type}, but got {type(e)}')
        else: raise AssertionError(f'Expected exception {exception_type}, but no exception was raised')
    
    def status_code(self, response, expected_code, message=None):
        actual = getattr(response, 'status_code', None)
        if actual != expected_code: raise AssertionError(message or f'Expected status {expected_code}, got {actual}')
    
    def json_equal(self, response, key, expected_code, message=None):
        try: data = response.json()
        except Exception as e: raise AssertionError(message or 'Response is not valid JSON')
        
        actual = data.get(key)
        if actual != expected_code: raise AssertionError(message or f'Expected JSON[{key}]={expected_code}, got {actual}')
        
    