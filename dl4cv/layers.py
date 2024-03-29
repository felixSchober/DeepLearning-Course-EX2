import numpy as np


def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    #############################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You     #
    # will need to reshape the input into rows.                                 #
    #############################################################################
    x_row = np.reshape(x, (x.shape[0], -1))
    out = np.dot(x_row, w) + b

    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    #############################################################################
    # TODO: Implement the affine backward pass.                                 #
    #############################################################################
    x_row = np.reshape(x, (x.shape[0], -1))

    dw = np.dot(x_row.T, dout)
    db = np.sum(dout, axis=0, keepdims=False)
    dx_row = np.dot(dout, w.T)
    dx = dx_row.reshape(x.shape)

#############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    #############################################################################
    # TODO: Implement the ReLU forward pass.                                    #
    #############################################################################
    out = x * (x > 0)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    #############################################################################
    # TODO: Implement the ReLU backward pass.                                   #
    #############################################################################

    # derivative of relu is
    # dRelu(0) = 0
    # dRelu(>0) = 1
    dx = np.array(dout, copy=True)
    dx[x <= 0] = 0
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
    return dx


def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the mean
    and variance of each feature, and these averages are used to normalize data
    at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7 implementation
    of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == 'train':
        #############################################################################
        # TODO: Implement the training-time forward pass for batch normalization.   #
        # Use minibatch statistics to compute the mean and variance, use these      #
        # statistics to normalize the incoming data, and scale and shift the        #
        # normalized data using gamma and beta.                                     #
        #                                                                           #
        # You should store the output in the variable out. Any intermediates that   #
        # you need for the backward pass should be stored in the cache variable.    #
        #                                                                           #
        # You should also use your computed sample mean and variance together with  #
        # the momentum variable to update the running mean and running variance,    #
        # storing your result in the running_mean and running_var variables.        #
        #############################################################################
        sample_mean = np.mean(x, axis=0)

        x_minus_mean = x - sample_mean

        sq = x_minus_mean ** 2

        var = 1. / N * np.sum(sq, axis=0)

        sqrtvar = np.sqrt(var + eps)

        ivar = 1. / sqrtvar

        x_norm = x_minus_mean * ivar

        gammax = gamma * x_norm

        out = gammax + beta

        running_var = momentum * running_var + (1 - momentum) * var
        running_mean = momentum * running_mean + (1 - momentum) * sample_mean

        cache = (out, x_norm, beta, gamma, x_minus_mean, ivar, sqrtvar, var, eps)

        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
    elif mode == 'test':
        #############################################################################
        # TODO: Implement the test-time forward pass for batch normalization. Use   #
        # the running mean and variance to normalize the incoming data, then scale  #
        # and shift the normalized data using gamma and beta. Store the result in   #
        # the out variable.                                                         #
        #############################################################################
        x = (x - running_mean) / np.sqrt(running_var)
        out = x * gamma + beta
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    #############################################################################
    # TODO: Implement the backward pass for batch normalization. Store the      #
    # results in the dx, dgamma, and dbeta variables.                           #
    #############################################################################

    xout, x_norm, beta, gamma, x_minus_mean, ivar, sqrtvar, var, eps = cache
    N, D = dout.shape

    # step 1 (+ Operation) - dx => 1 * dout
    dbeta = np.sum(dout, axis=0)
    dgammax = dout

    # step 2 (* Operation)
    # dgamma = x * dout(dgammax)
    # dxnorm = gamma * dout(dgammax)
    dgamma = np.sum(dgammax * xout, axis=0)
    dx_norm = gamma * dgammax

    # step 3 (* Operation: minus_mean * ivar)
    # divar = dx_norm * minus_mean
    # dminus_mean = dx_norm * ivar
    divar = np.sum(dx_norm * x_minus_mean, axis=0)
    dminus_mean_1 = dx_norm * ivar

    # step 4 (div Operation: 1 / sqrtvar)
    # dsqrtvar = divar * ( - 1 / sqrtVar^2)
    dsqrtvar = divar * ( - 1.0 / (sqrtvar ** 2))

    # step 5 (sqrt(x+eps))
    # dvar = dsqrtvar * 1.0 / (2 * sqrt(var + eps))
    dvar = dsqrtvar * (1.0 / (2 * np.sqrt(var + eps)))

    # step 6 (1/N sum)
    # dsq = 1/N * dvar
    dsq = (1.0 / N) * np.ones((N, D)) * dvar

    # step 7 (** 2)
    # dminus_mean_2 = 2 * x_minus_mean * dsq
    dminus_mean_2 = 2 * x_minus_mean * dsq

    # step 8 ( x - x_mean)
    # dx = dminus_mean_2 + dminus_mean_1
    # dsample_mean = - (dminus_mean_2 + dminus_mean_1)
    dx1 = dminus_mean_2 + dminus_mean_1
    dsample_mean = - np.sum(dminus_mean_2 + dminus_mean_1, axis=0)

    # step 9 (mean)
    # dx2 = 1/N * dsample_mean
    dx2 = (1.0 / N) * np.ones((N, D)) * dsample_mean

    # last step: combination
    dx = dx1 + dx2

    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################

    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We drop each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not in
        real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        ###########################################################################
        # TODO: Implement the training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                            #
        ###########################################################################

        # randomly scale (some) activations by (some) amount
        # (usually the reciprocal of the dropout parameter).

        # creates a mask with [True, False, ...] depending on the value of p. Then divide that by reciprocal of p
        # so that we have (random) activation scaling [0, 0, 2] (in case of p = 0.5 (because True => 1.0)
        mask = (np.random.rand(*x.shape) >= p) / (1 - p)
        out = x * mask

        ###########################################################################
        #                            END OF YOUR CODE                             #
        ###########################################################################
    elif mode == 'test':
        ###########################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.       #
        ###########################################################################

        # nothing to do here
        out = x

        ###########################################################################
        #                            END OF YOUR CODE                             #
        ###########################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']

    dx = None
    if mode == 'train':
        ###########################################################################
        # TODO: Implement the training phase backward pass for inverted dropout.  #
        ###########################################################################

        dx = dout * mask

        ###########################################################################
        #                            END OF YOUR CODE                             #
        ###########################################################################
    elif mode == 'test':
        dx = dout
    return dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
      for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    probs = np.exp(x - np.max(x, axis=1, keepdims=True))
    probs /= np.sum(probs, axis=1, keepdims=True)
    N = x.shape[0]
    loss = -np.sum(np.log(probs[np.arange(N), y])) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx












# # Testing
# from dl4cv.classifiers.fc_net import *
# from dl4cv.data_utils import get_CIFAR10_data
# from dl4cv.gradient_check import eval_numerical_gradient, eval_numerical_gradient_array
# from dl4cv.solver import Solver
# def rel_error(x, y):
#     """ returns relative error """
#     return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))
# # data = get_CIFAR10_data()
# # for k, v in data.items():
# #     print('%s: ' % k, v.shape)
#
# # Test the affine_forward function
#
# num_inputs = 2
# input_shape = (4, 5, 6)
# output_dim = 3
#
# input_size = num_inputs * np.prod(input_shape)
# weight_size = output_dim * np.prod(input_shape)
#
# x = np.linspace(-0.1, 0.5, num=input_size).reshape(num_inputs, *input_shape)
# w = np.linspace(-0.2, 0.3, num=weight_size).reshape(np.prod(input_shape), output_dim)
# b = np.linspace(-0.3, 0.1, num=output_dim)
#
# out, _ = affine_forward(x, w, b)
# correct_out = np.array([[ 1.49834967,  1.70660132,  1.91485297],
#                         [ 3.25553199,  3.5141327,   3.77273342]])
#
# # Compare your output with ours. The error should be around 1e-9.
# print('Testing affine_forward function:')
# #print('difference: ', rel_error(out, correct_out))

# x = np.random.randn(10, 2, 3)
# w = np.random.randn(6, 5)
# b = np.random.randn(5)
# dout = np.random.randn(10, 5)
#
# dx_num = eval_numerical_gradient_array(lambda x: affine_forward(x, w, b)[0], x, dout)
# dw_num = eval_numerical_gradient_array(lambda w: affine_forward(x, w, b)[0], w, dout)
# db_num = eval_numerical_gradient_array(lambda b: affine_forward(x, w, b)[0], b, dout)
#
# _, cache = affine_forward(x, w, b)
# dx, dw, db = affine_backward(dout, cache)
#
# # The error should be around 1e-10
# print('Testing affine_backward function:')
# print('dx error: ', rel_error(dx_num, dx))
# print('dw error: ', rel_error(dw_num, dw))
# print('db error: ', rel_error(db_num, db))
